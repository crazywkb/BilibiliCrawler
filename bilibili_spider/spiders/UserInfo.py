# -*- coding: utf-8 -*-
import scrapy


class UserInfoSpider(scrapy.Spider):
    name = 'UserInfo'

    def parse(self, response):
        pass

    """
    1. 考虑专门使用一个爬虫进行用户的寻找，对每个找到的用户进行判断，如果用户等级为3级以下，则跳过，不收录。
    2. 爬取过程中，对于已经爬取过得用户，需要及时从数据集中移除。
    3. 从关注列表中和follower中寻找遍历，并搜索进行广度搜索。
    """
