from bilibili_spider.models import connect
from bilibili_spider.models import Animation
from bilibili_spider.models import AnimationFeature
from sqlalchemy.orm import sessionmaker


def get_Animation_media_list():
    Session = sessionmaker(bind=connect())
    session = Session()
    query = session.query(Animation.media_id)
    return [item[0] for item in query]


def get_AnimationFeature_media_list():
    Session = sessionmaker(bind=connect())
    session = Session()
    query = session.query(AnimationFeature.media_id)
    return [item[0] for item in query]


if __name__ == '__main__':
    media_list = get_Animation_media_list()
    test_list = get_AnimationFeature_media_list()
    print(set(media_list) - set(test_list))
    print(len(media_list), len(test_list))

