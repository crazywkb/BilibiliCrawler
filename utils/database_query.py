from bilibili_spider.models import connect
from bilibili_spider.models import Animation

from sqlalchemy.orm import sessionmaker


def get_media_list():
    Session = sessionmaker(bind=connect())
    session = Session()
    query = session.query(Animation.media_id)
    return [item[0] for item in query]
