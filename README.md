# BilibiliAnimationRecommender
## Description
Data collector and analyzer for data mining course's final project, aiming at making a more accurate algorithm to do animation recommendation.

## Structure
```text
BilibiliAnimationRecommender
    - bilibili_analyzer 
    - bilibili_spider  # web spiders for crawling bilibili animation and user information.
        - spiders
            - Animation.py  # spider for crawling animation information in detail
            - AnimationFeature.py  # spider for crawling animation extra features
            - UserInfo.py  # spider for crawling user info and preferences
        - items.py
        - middlewares.py
        - models.py  # sqlalchemy models
        - pipelines.py
        - settings.py
    - migrates
        - versions  # history of database changing
        - ...
    - utils
    - alembic.ini
    - scrapy.cfg
```
