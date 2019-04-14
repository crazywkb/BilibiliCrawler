# -*- coding: utf-8 -*-
from scrapy import Item, Field


class AnimationItem(Item):
    link = Field()
    is_finish = Field()
    media_id = Field()
    follow = Field()
    play = Field()
    pub_date = Field()
    pub_real_time = Field()
    renewal_time = Field()
    score = Field()
    season_id = Field()
    title = Field()


class AnimationFeatureItem(Item):
    media_id = Field()
    tag_list = Field()  # 番剧标签
    review_times = Field()  # 评分人数
    character_voice_list = Field()  # 声优列表，json.loads()
    character_staff_list = Field()  # 导演、编剧等 json.loads()
    short_comment_sum = Field()  # 短评总数
    long_comment_sum = Field()  # 长评总数
