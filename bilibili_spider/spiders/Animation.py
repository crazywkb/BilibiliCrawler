# -*- coding: utf-8 -*-
import json

import scrapy
from w3lib.url import add_or_replace_parameters as url_encode

from bilibili_spider.items import AnimationItem


class AnimationSpider(scrapy.Spider):
    name = 'Animation'

    url = 'http://bangumi.bilibili.com/media/web_api/search/result'
    spider_params = {
        'page': 1,
        'season_type': 1
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'bilibili_spider.pipelines.MysqlPipeline': 100
        }
    }

    proxy_num = 20

    def start_requests(self):
        yield scrapy.Request(url_encode(self.url, self.spider_params), callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            data_list = json.loads(response.text).get('result', dict()).get('data', list())

        except json.JSONDecodeError:
            self.logger.error("Error occur while decoding response in Animation.")
            yield scrapy.Request(url=url_encode(self.url, self.spider_params), callback=self.parse, dont_filter=True)

        else:
            for item in data_list:
                animation = AnimationItem()
                animation['link'] = item.get('link', None)
                animation['is_finish'] = item.get('is_finish', None)
                animation['media_id'] = item.get('media_id', None)
                animation['season_id'] = item.get('season_id', None)
                animation['title'] = item.get('title', None)

                animation['follow'] = item.get('order', dict()).get('follow', None)
                animation['play'] = item.get('order', dict()).get('play', None)
                animation['pub_date'] = item.get('order', dict()).get('pub_date', None)
                animation['pub_real_time'] = item.get('order', dict()).get('pub_real_time', None)
                animation['renewal_time'] = item.get('order', dict()).get('renewal_time', None)
                animation['score'] = item.get('order', dict()).get('score', None)

                yield animation

            if len(data_list):
                self.spider_params['page'] += 1
                yield scrapy.Request(url=url_encode(self.url, self.spider_params), callback=self.parse, dont_filter=True)
