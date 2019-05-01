# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random

import requests
from scrapy import signals
from scrapy.utils.project import get_project_settings
from twisted.internet.error import TimeoutError


class BilibiliSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BilibiliSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware(object):
    proxy_list = None
    get_proxy_url = None
    proxy_num = None
    useful_proxy_sum = None

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def __get_proxy_list(self, proxy_num):
        raw_list = requests.get(self.get_proxy_url % proxy_num).json()
        proxy_list = []
        for item in raw_list:
            proxy = item.get('https', None)
            if not proxy:
                proxy = item['http']
            proxy_list.append(proxy)
        self.proxy_list = proxy_list
        self.proxy_num = self.useful_proxy_sum = len(self.proxy_list)

    def spider_opened(self, spider):
        self.get_proxy_url = get_project_settings().get('PROXY_URL')
        self.__get_proxy_list(spider.proxy_num)

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.proxy_list)

    def process_response(self, request, response, spider):
        if response.status != 200:
            try:
                self.proxy_list.remove(request.meta['proxy'])
                self.useful_proxy_sum -= 1

            except ValueError:
                pass

            spider.logger.warn(f"Access error while using proxy. status {response.status}. {self.useful_proxy_sum}/{self.proxy_num} {len(self.proxy_list)}")
            if not self.useful_proxy_sum:
                self.__get_proxy_list(spider.proxy_num)
                spider.logger.warn(f"Proxy pool exhausted. Get {self.useful_proxy_sum} proxy again.")

            request.meta['proxy'] = random.choice(self.proxy_list)
            return request

        return response

    def process_exception(self, request, exception, spider):
        try:
            self.proxy_list.remove(request.meta['proxy'])
            self.useful_proxy_sum -= 1

        except ValueError:
            pass

        spider.logger.warn(f"Timeout while using proxy. {self.useful_proxy_sum}/{self.proxy_num} {len(self.proxy_list)}")

        if not self.useful_proxy_sum:
            self.__get_proxy_list(spider.proxy_num)
            spider.logger.warn(f"Proxy pool exhausted. Get {self.useful_proxy_sum} proxy again.")

        request.meta['proxy'] = random.choice(self.proxy_list)
        return request
