# -*- coding: utf-8 -*-
import scrapy


class AnimationCommentSpider(scrapy.Spider):
    name = 'AnimationComment'
    allowed_domains = ['test.com']
    start_urls = ['http://test.com/']

    def parse(self, response):
        pass
