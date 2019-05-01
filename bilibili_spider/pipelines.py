# -*- coding: utf-8 -*-
import importlib

from sqlalchemy.orm import sessionmaker

from bilibili_spider.models import connect, create_table


class MysqlPipeline(object):
    def __init__(self):
        engine = connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        model_class = getattr(importlib.import_module('bilibili_spider.models'), spider.name)  # fuck you
        model = model_class()
        model.update(**item)

        try:
            session.add(model)
            session.commit()
        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item


class MysqlAdvancedPipeline(object):
    def __init__(self):
        engine = connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        model_class = getattr(importlib.import_module('bilibili_spider.models'), item.__reflect__)  # fuck you
        model = model_class()
        model.update(**item)

        try:
            session.add(model)
            session.commit()
        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item