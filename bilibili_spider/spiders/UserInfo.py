# -*- coding: utf-8 -*-
import json

import redis
import scrapy
from scrapy.utils.project import get_project_settings
from w3lib.url import add_or_replace_parameter
from utils.url_operation import get_param_value
from bilibili_spider.items import UserInfoItem
from bilibili_spider.items import UserStatItem
from bilibili_spider.items import UserUpStatItem


class UserInfoSpider(scrapy.Spider):
    name = 'UserInfo'
    start_mid = 52491871
    redis = None

    __key_of_redis_users = 'finished_users'
    proxy_num = 500

    fan_url = 'https://api.bilibili.com/x/relation/followers?vmid=%s&pn=1&ps=50&order=desc'
    following_url = 'https://api.bilibili.com/x/relation/followings?vmid=%s&pn=1&ps=50&order=desc'
    user_info_url = 'https://api.bilibili.com/x/space/acc/info?mid=%s'
    stat_url = 'https://api.bilibili.com/x/relation/stat?vmid=%s'
    upstat_url = 'https://api.bilibili.com/x/space/upstat?mid=%s'
    animation_following_url = 'https://api.bilibili.com/x/space/bangumi/follow/list?type=1&pn=%s&ps=50&vmid=%s'

    __page_limitation = 5
    custom_settings = {
        'ITEM_PIPELINES': {
            'bilibili_spider.pipelines.MysqlAdvancedPipeline': 100
        }
    }

    def start_requests(self):
        self.redis = redis.Redis(**get_project_settings().get('REDIS_SETTINGS'))
        self.redis.sadd(self.__key_of_redis_users, '')
        yield scrapy.Request(self.user_info_url % self.start_mid, callback=self.parse_user_info, dont_filter=True)

    def parse(self, response):
        pass

    def __user_exist(self, mid):
        return self.redis.sismember(self.__key_of_redis_users, mid)

    def __is_qualified(self, user):
        """
        check whether user qualified.
        :param user: a dict contains user info
        :return: boolean
        """
        if not user:
            return False

        level_qualified = user.get('level', 0) > 2
        if not level_qualified:
            return False

        # do not return in one line, it will cost an extra connection.
        user_exist = self.__user_exist(user.get('mid', 0))
        if user_exist:
            return False

        return True

    def __add_user_redis(self, mid):
        return self.redis.sadd(self.__key_of_redis_users, mid)

    def __add_following_set2user(self, mid, media_id_list):
        if not media_id_list:
            return None
        else:
            return self.redis.sadd(mid, *media_id_list)

    def parse_user_info(self, response):
        data = json.loads(response.text).get('data', dict())
        if not data:
            return

        if not self.__is_qualified(data):
            self.logger.info(f'{data.get("mid", 0)} is not qualified.')
            return

        user = UserInfoItem()
        official = data.get('official', dict())
        vip = data.get('vip', dict())

        user['mid'] = data.get('mid')
        user['name'] = data.get('name')
        user['sign'] = data.get('sign', None)
        user['rank'] = data.get('rank')
        user['level'] = data.get('level')
        user['jointime'] = data.get('jointime')
        user['moral'] = data.get('moral')
        user['silence'] = data.get('silence')
        user['birthday'] = data.get('birthday', None)
        user['coins'] = data.get('coins')
        user['fans_badge'] = data.get('fans_badge')

        user['role'] = official.get('role')
        user['title'] = official.get('title', None)
        user['desc'] = official.get('desc', None)

        user['vip_type'] = vip.get('type')
        user['vip_status'] = vip.get('status')

        self.logger.info(f"Crawled user {user['mid']} info.")
        self.__add_user_redis(user['mid'])

        yield user

        mid = user['mid']  # avoid memory leakage

        yield scrapy.Request(self.upstat_url % mid, callback=self.parse_upstat, dont_filter=True)
        yield scrapy.Request(self.stat_url % mid, callback=self.parse_stat, dont_filter=True)
        yield scrapy.Request(self.animation_following_url % (1, mid), callback=self.parse_animation_following_list, dont_filter=True)
        yield scrapy.Request(self.fan_url % mid, callback=self.parse_fan_or_following_list, dont_filter=True)
        yield scrapy.Request(self.following_url % mid, callback=self.parse_fan_or_following_list, dont_filter=True)

    def parse_stat(self, response):
        data = json.loads(response.text).get('data', dict())
        stat = UserStatItem()
        stat['mid'] = data.get('mid')
        stat['following'] = data.get('following')
        stat['whisper'] = data.get('whisper')
        stat['black'] = data.get('black')
        stat['follower'] = data.get('follower')

        self.logger.info(f"Crawled user {stat['mid']} stat")
        yield stat

    def parse_upstat(self, response):
        data = json.loads(response.text).get('data', dict())
        upstat = UserUpStatItem()
        upstat['mid'] = get_param_value(response.request.url, 'mid')
        upstat['archive_view'] = data.get('archive', dict()).get('view')
        upstat['article_view'] = data.get('article', dict()).get('view')

        self.logger.info(f"Crawled user {upstat['mid']} upstat.")
        yield upstat

    def parse_fan_or_following_list(self, response):
        data = json.loads(response.text).get('data', dict())

        fan_list = data.get('list', list())  # avoid errors caused by limitation of reading pages.
        for fan in fan_list:
            yield scrapy.Request(self.user_info_url % fan.get('mid'), callback=self.parse_user_info, dont_filter=True)

        url = response.request.url
        vmid = get_param_value(url, 'vmid')

        if not fan_list:
            self.logger.info(f"Crawled user {vmid} fans or following done.")
        else:
            page_num = int(get_param_value(url, 'pn')) + 1
            url = add_or_replace_parameter(url, 'pn', page_num)
            yield scrapy.Request(url, callback=self.parse_fan_or_following_list, dont_filter=True)

    def parse_animation_following_list(self, response):
        data = json.loads(response.text).get('data', dict())
        animation_list = data.get('list', list())
        animation_following_list = list()

        for animation in animation_list:
            animation_following_list.append(animation.get('media_id'))

        url = response.request.url
        vmid = get_param_value(url, 'vmid')
        pn = get_param_value(url, 'pn')

        if not animation_following_list:
            self.logger.info(f"Crawled user {vmid} done.")

        else:
            self.__add_following_set2user(vmid, animation_following_list)
            pn = int(pn) + 1
            url = add_or_replace_parameter(url, 'pn', pn)
            yield scrapy.Request(url, callback=self.parse_animation_following_list, dont_filter=True)
