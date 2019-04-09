from scrapy.utils.project import get_project_settings as __get_project_settings
from sqlalchemy import Column
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
    media_id = Column(Integer)
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
