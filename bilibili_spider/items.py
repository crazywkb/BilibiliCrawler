# -*- coding: utf-8 -*-
from scrapy import Item, Field


class AnimationItem(Item):
    __reflect__ = 'Animation'
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
    __reflect__ = 'AnimationFeature'
    media_id = Field()
    tag_list = Field()  # 番剧标签
    review_times = Field()  # 评分人数
    character_voice_list = Field()  # 声优列表，json.loads()
    character_staff_list = Field()  # 导演、编剧等 json.loads()
    short_comment_sum = Field()  # 短评总数
    long_comment_sum = Field()  # 长评总数


class UserInfoItem(Item):
    __reflect__ = 'UserInfo'
    mid = Field()
    name = Field()
    sex = Field()
    sign = Field()
    rank = Field()  # 讲道理我也不知道是啥
    level = Field()
    jointime = Field()
    moral = Field()
    silence = Field()
    birthday = Field()
    coins = Field()
    fans_badge = Field()
    role = Field()
    title = Field()
    desc = Field()
    vip_type = Field()
    vip_status = Field()


class UserUpStatItem(Item):
    __reflect__ = 'UserUpStat'
    mid = Field()
    archive_view = Field()
    article_view = Field()


class UserStatItem(Item):
    __reflect__ = 'UserStat'
    mid = Field()
    following = Field()
    black = Field()
    whisper = Field()
    follower = Field()
