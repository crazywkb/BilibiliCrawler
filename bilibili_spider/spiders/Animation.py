# -*- coding: utf-8 -*-
from w3lib.url import add_or_replace_parameters as url_encode
import json
import scrapy
from scrapy.crawler import CrawlerProcess


class AnimationSpider(scrapy.Spider):
    name = 'Animation'
    spider_params = {
        'page': 1,
        'season_type': 1
    }
    url = 'https://bangumi.bilibili.com/media/web_api/search/result'

    def start_requests(self):
        yield scrapy.Request(url_encode(self.url, self.spider_params), callback=self.parse)

    def parse(self, response):
        print(response.url)
        yield json.loads(response.text)


if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(AnimationSpider)
    process.start()  # the script will block here until the crawling is finished
