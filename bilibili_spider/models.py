from scrapy.utils.project import get_project_settings as __get_project_settings
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, Float, Boolean, Text
from sqlalchemy import create_engine as __create_engine
from sqlalchemy.ext.declarative import declarative_base as __declarative_base

TableBase = __declarative_base()


def connect():
    return __create_engine(__get_project_settings().get('CONNECTION_STRING'))


def create_table(engine):
    return TableBase.metadata.create_all(engine)


class Animation(TableBase):
    __tablename__ = "animation"

    id = Column(Integer, primary_key=True)
    link = Column(String(100))
    is_finish = Column(Boolean)
    media_id = Column(Integer, index=True)
    follow = Column(String(20))
    play = Column(String(20))
    pub_date = Column(Integer)
    pub_real_time = Column(Integer)
    renewal_time = Column(Integer)
    score = Column(Float)
    season_id = Column(Integer)
    title = Column(Text())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class AnimationFeature(TableBase):
    __tablename__ = "animation_feature"

    id = Column(Integer, primary_key=True)
    media_id = Column(Integer, ForeignKey(Animation.media_id))
    tag_list = Column(Text())
    review_times = Column(Integer)
    character_voice_list = Column(Text())
    character_staff_list = Column(Text())
    short_comment_sum = Column(Integer)
    long_comment_sum = Column(Integer)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class UserInfo(TableBase):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True)
    mid = Column(Integer, index=True)
    name = Column(String(50))
    sex = Column(String(10))
    sign = Column(Text())
    rank = Column(Integer)
    level = Column(Integer)
    jointime = Column(Integer)
    moral = Column(Integer)
    silence = Column(Integer)
    birthday = Column(String(20))
    coins = Column(Integer)
    fans_badge = Column(Boolean)
    role = Column(Integer)
    title = Column(Text())
    desc = Column(Text())
    vip_type = Column(Integer)
    vip_status = Column(Integer)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class UserUpStat(TableBase):
    __tablename__ = "user_upstat"

    id = Column(Integer, primary_key=True)
    mid = Column(Integer, ForeignKey(UserInfo.mid))
    archive_view = Column(Integer)
    article_view = Column(Integer)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class UserStat(TableBase):
    __tablename__ = "user_stat"

    id = Column(Integer, primary_key=True)
    mid = Column(Integer, ForeignKey(UserInfo.mid))
    following = Column(Integer)
    whisper = Column(Integer)
    black = Column(Integer)
    follower = Column(Integer)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
