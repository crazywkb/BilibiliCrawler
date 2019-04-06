# -*- coding: utf-8 -*-
import scrapy


class UserInfoSpider(scrapy.Spider):
    name = 'UserInfo'
    allowed_domains = ['test.com']
    start_urls = ['http://test.com/']

    def parse(self, response):
        pass
