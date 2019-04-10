# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker

from bilibili_spider.models import connect, create_table


class AnimationMysqlPipeline(object):
    def __init__(self):
        engine = connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, spider):
        session = self.Session()
        pass

        try:
            session.commit()
        except:
            session.rollback()
            raise

        finally:
            session.close()

        return None
