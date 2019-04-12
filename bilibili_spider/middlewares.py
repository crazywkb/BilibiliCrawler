# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import requests
import random


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
    retry_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def __get_proxy_list(self, proxy_num):
        raw_list = requests.get("http://139.199.98.197:3289/get/" + str(proxy_num)).json()
        proxy_list = []
        for item in raw_list:
            proxy = item.get('https', None)
            if not proxy:
                proxy = item['http']
            proxy_list.append(proxy)
        self.proxy_list = proxy_list

    def spider_opened(self, spider):
        self.__get_proxy_list(spider.proxy_num)

        spider.logger.info(f"Load {len(self.proxy_list)} proxy in spider")

    def process_request(self, request, spider):
        request.meta['proxy'] = random.choice(self.proxy_list)

    def process_response(self, request, response, spider):
        if response.status == 200:
            self.retry_count = 0

        else:
            proxy = request.meta['proxy']
            request.meta['proxy'] = random.choice(self.proxy_list)
            self.retry_count += 1
            self.proxy_list.remove(proxy)

            if not len(self.proxy_list):
                self.__get_proxy_list(spider.proxy_num)

        print("+" * 100)
        print(request.meta)
        return response

    def process_exception(self, request, exception, spider):
        if self.retry_count >= spider.proxy_num:
            self.__get_proxy_list(spider.proxy_num)

            spider.logger.warn(f"Proxy may be exhausted, reload {len(self.proxy_list)} proxy.")
            self.retry_count = 0

        else:
            proxy = request.meta['proxy']
            self.retry_count += 1
            self.proxy_list.remove(proxy)

            if not len(self.proxy_list):
                self.__get_proxy_list(spider.proxy_num)

        request.meta['proxy'] = random.choice(self.proxy_list)
        return request
