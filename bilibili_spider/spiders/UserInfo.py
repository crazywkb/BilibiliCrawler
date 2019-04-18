# -*- coding: utf-8 -*-
import scrapy


class UserInfoSpider(scrapy.Spider):
    name = 'UserInfo'

    fan_url = 'https://api.bilibili.com/x/relation/followers?vmid=%s&pn=%s&ps=50&order=desc'
    following_url = 'https://api.bilibili.com/x/relation/followings?vmid=%s&pn=%s&ps=50&order=desc'
    user_info_url = 'https://api.bilibili.com/x/space/acc/info?mid=%s'
    stat_url = 'https://api.bilibili.com/x/relation/stat?vmid=%s'
    upstat_url = 'https://api.bilibili.com/x/space/upstat?mid=%s'
    animation_following_url = 'https://api.bilibili.com/x/space/bangumi/follow/list?type=1&pn=%s&ps=50&vmid=%s'

    def start_requests(self):
        # 遍历所有fan和follower，然后yield出request去请求info信息，然后yield去请求追番信息。
        pass

    def parse(self, response):
        pass

    """
    1. 考虑专门使用一个爬虫进行用户的寻找，对每个找到的用户进行判断，如果用户等级为3级以下，则跳过，不收录。
    2. 爬取过程中，对于已经爬取过得用户，需要及时从数据集中移除。
    3. 从关注列表中和follower中寻找遍历，并搜索进行广度搜索。
    """
