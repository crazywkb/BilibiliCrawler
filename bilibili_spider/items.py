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
