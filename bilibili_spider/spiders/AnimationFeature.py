# -*- coding: utf-8 -*-
import scrapy
import re
from utils.database_query import get_media_list
from bilibili_spider.items import AnimationFeatureItem


class AnimationCommentSpider(scrapy.Spider):
    name = 'AnimationFeature'

    url = 'https://www.bilibili.com/bangumi/media/md%s/'
    media_list = None

    proxy_num = 20
    long_comment_sum_patter = r'长评 \( (*.?) \)'

    custom_settings = {
        'ITEM_PIPELINES': {
            'bilibili_spider.pipelines.MysqlPipeline': 100
        }
    }

    def start_requests(self):
        media_list = get_media_list()

        for media_id in media_list:
            yield scrapy.Request(url=self.url % media_id, callback=self.parse, dont_filter=True)

    def parse(self, response):
        review_times = response.xpath('//div[@class="media-info-review-times"]/text()').extract_first()
        tag_list = response.xpath("//span[@class='media-tag']/text()").extract()
        comment_sum_list = response.xpath("//ul[@class='clearfix']/li/text()").extract()[1:]

        feature = AnimationFeatureItem()
        feature['review_times'] = str(review_times)
        feature['tag_list'] = str(tag_list)
        feature['media_id'] = 5789

        yield feature
