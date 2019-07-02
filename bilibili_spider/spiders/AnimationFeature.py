# -*- coding: utf-8 -*-
import json
import re

import scrapy

from bilibili_spider.items import AnimationFeatureItem
from utils.database_query import get_Animation_media_list


class AnimationCommentSpider(scrapy.Spider):
    name = 'AnimationFeature'

    url = 'https://www.bilibili.com/bangumi/media/md%s/'

    proxy_num = 100
    long_comment_sum_pattern = r'长评 \( (\d*) \)'
    short_comment_sum_pattern = r'短评 \( (\d*) \)'
    voice_and_staff_pattern = r'(\{.*\});'

    custom_settings = {
        'ITEM_PIPELINES': {
            'bilibili_spider.pipelines.MysqlPipeline': 100
        }
    }

    def start_requests(self):
        media_list = get_Animation_media_list()

        for media_id in media_list:
            request = scrapy.Request(url=self.url % media_id, callback=self.parse, dont_filter=True)
            request.meta['media_id'] = media_id
            self.logger.info(f"Start to crawl {request.url}")
            yield request

    def parse(self, response):
        review_times = response.xpath('//div[@class="media-info-review-times"]/text()').extract_first()
        tag_list = response.xpath("//span[@class='media-tag']/text()").extract()

        feature = AnimationFeatureItem()
        feature['media_id'] = response.request.meta['media_id']
        feature['review_times'] = str(review_times)
        feature['tag_list'] = json.dumps(tag_list)

        comment_sum_list = response.xpath("//ul[@class='clearfix']/li/text()").extract()[1:]

        long_comment_sum = 0
        short_comment_sum = 0
        if comment_sum_list:
            temp_long = re.search(self.long_comment_sum_pattern, comment_sum_list[0])
            temp_short = re.search(self.long_comment_sum_pattern, comment_sum_list[1])
            if temp_long:
                long_comment_sum = temp_long.groups()[0]
            if temp_short:
                short_comment_sum = temp_short.groups()[0]

        feature['long_comment_sum'] = long_comment_sum
        feature['short_comment_sum'] = short_comment_sum

        voice_and_staff_groups = re.search(self.voice_and_staff_pattern, response.text).groups()
        voice_dict = dict()
        staff_dict = dict()

        if len(voice_and_staff_groups):
            voice_and_staff_json = json.loads(voice_and_staff_groups[0])

            voice_raw = voice_and_staff_json['mediaInfo']['actors'].strip().split('\n')
            for role_actor in voice_raw:
                if not role_actor:
                    continue

                try:
                    role, actor = re.split('[:：]', role_actor, maxsplit=1)
                    voice_dict[role.strip()] = actor
                except:
                    self.logger.warn(f"Error occur in CV: {role_actor}, url: {response.url}")
                    continue

            staff_raw = voice_and_staff_json['mediaInfo']['staff'].strip().split('\n')
            for staff_person in staff_raw:
                if not staff_person:
                    continue

                try:
                    staff, person = re.split('[:：]', staff_person, maxsplit=1)
                    staff_dict[staff] = person
                except:
                    self.logger.warn(f"Error occur in staff: {staff_person}, url: {response.url}")
                    continue

        feature['character_voice_list'] = json.dumps(voice_dict)
        feature['character_staff_list'] = json.dumps(staff_dict)

        self.logger.info(f"crawl {response.url} done and yield Item.")
        yield feature
