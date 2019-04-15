# -*- coding: utf-8 -*-
import scrapy
import re
from utils.database_query import get_media_list
from bilibili_spider.items import AnimationFeatureItem
import json


class AnimationCommentSpider(scrapy.Spider):
    name = 'AnimationFeature'

    url = 'https://www.bilibili.com/bangumi/media/md%s/'
    media_list = None

    proxy_num = 20
    long_comment_sum_pattern = r'长评 \( (\d*) \)'
    short_comment_sum_pattern = r'短评 \( (\d*) \)'
    voice_and_staff_pattern = r'(\{.*\});'

    custom_settings = {
        'ITEM_PIPELINES': {
            'bilibili_spider.pipelines.MysqlPipeline': 100
        }
    }

    def start_requests(self):
        media_list = get_media_list()

        for media_id in media_list:
            request = scrapy.Request(url=self.url % media_id, callback=self.parse, dont_filter=True)
            request.meta['media_id'] = media_id
            yield request

    def parse(self, response):
        review_times = response.xpath('//div[@class="media-info-review-times"]/text()').extract_first()
        tag_list = response.xpath("//span[@class='media-tag']/text()").extract()

        feature = AnimationFeatureItem()
        feature['media_id'] = response.request.meta['media_id']
        feature['review_times'] = str(review_times)
        feature['tag_list'] = json.dumps(tag_list)

        comment_sum_list = response.xpath("//ul[@class='clearfix']/li/text()").extract()[1:]
        if not comment_sum_list:
            long_comment_sum = 0
            short_comment_sum = 0
        else:
            long_comment_sum = re.search(self.long_comment_sum_pattern, comment_sum_list[1]).groups()[0]
            short_comment_sum = re.search(self.long_comment_sum_pattern, comment_sum_list[2]).groups()[0]

        feature['long_comment_sum'] = long_comment_sum
        feature['short_comment_sum'] = short_comment_sum

        voice_and_staff_groups = re.search(self.voice_and_staff_pattern, response.text).groups()
        voice_dict = dict()
        staff_dict = dict()

        if not len(voice_and_staff_groups):
            voice_and_staff_json = json.loads(voice_and_staff_groups[0])
            voice_raw = voice_and_staff_json['mediaInfo']['actors'].split('\n')
            for role_actor in voice_raw:
                role, actor = role_actor.split('：')
                voice_dict[role] = actor

            staff_raw = voice_and_staff_json['mediaInfo']['staff'].split('\n')
            for staff_person in staff_raw:
                staff, person = staff_person.split('：')
                staff_dict[staff] = person

        feature['character_voice_list'] = json.dumps(voice_dict)
        feature['character_staff_list'] = json.dumps(staff_dict)

        yield feature
