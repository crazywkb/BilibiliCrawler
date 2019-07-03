---
layout: page
mathjax: true
permalink: /2019/projects/p07/midterm/
---

## 项目进展报告

### 数据获取及预处理

#### 数据来源

所有数据从bilibili主站直接爬取，通过分析网页中数据加载时的API来源获取相关信息，对应的API与信息如下：

| API                                                          | 信息         |
| :----------------------------------------------------------- | ------------ |
| http://bangumi.bilibili.com/media/web_api/search/result      | 番剧列表     |
| https://www.bilibili.com/bangumi/media/md%s/                 | 番剧详细信息 |
| https://api.bilibili.com/x/relation/followers?vmid=%s&pn=1&ps=50&order=desc | 用户粉丝列表 |
| https://api.bilibili.com/x/relation/followings?vmid=%s&pn=1&ps=50&order=desc | 用户关注列表 |
| https://api.bilibili.com/x/space/acc/info?mid=%s             | 用户信息     |
| https://api.bilibili.com/x/relation/stat?vmid=%s             | 用户特征信息 |
| https://api.bilibili.com/x/space/upstat?mid=%s               | 用户投稿信息 |
| https://api.bilibili.com/x/space/bangumi/follow/list?type=1&pn=%s&ps=50&vmid=%s | 番剧收藏列表 |



#### 技术框架

| 框架/语言  | 版本信息 | 用途               |
| ---------- | -------- | ------------------ |
| python     | 3.7.0    | 实现语言           |
| scrapy     | 1.6.0    | 爬虫框架           |
| sqlalchemy | 1.3.2    | orm工具            |
| alembic    | 1.0.8    | 数据库版本管理工具 |



#### 技术要点

* 网站反爬措施
  1. 针对`bilibili`的反爬措施，除去简单的使用`fake-useragent`进行替换以外，还另外构建一个简单爬虫，从各免费代理网站上爬取并维护IP池，当发送爬取信息请求时，从IP池中获取代理IP进行，以防当爬取速度过快时，本机IP被封锁的风险。
  2. 另外`scrapy`中缺少符合要求的`proxy`中间件，所以自行实现`scrapy`中的`middleware`部分。
  3. 通过API中的参数推断，突破对访问列表的限制（原始只能访问前200记录，修改后可访问500条）。
  4. 可分布式爬取。

* 数据存储部分
  1. `scrapy`框架中，数据存储偏向于`orm`类型，所以数据存储上，为了更好的兼容，使用了`sqlalchemy`来定义管理数据表结构，但是`sqlalchemy`缺少完善的版本管理工具，所以使用`alembic`提供管理。
  2. 数据的`pipeline`部分与`model`部分在原框架中只能一一对应，为了避免重复性工作，通过`python`的反射机制实现`pipeline`的一对多方法。
  3. 用户番剧收藏信息存在`redis`数据库中，可以用户爬取过程中的去重操作，其他信息存在`mariadb`中。



#### 数据处理

数据预处理过程中，设置以下规则对数据进行操作：

1. 数据去重
2. 对于用户等级小于2级的用户，不记录
3. 对于处于小黑屋状态的用户，不记录
4. 对于不开放番剧收藏的用户，不记录



#### 困难

大作业的完成过程中，由于我对数据库的不安全设置，导致数据被黑客清空，并索要酬金，后续重新爬取了相关数据，导致后续工作有延迟。

![](https://ws1.sinaimg.cn/large/005J7jqOly1g4moosjbjkj30zd0qygoi.jpg)



### 数据分析与可视化



### 模型选取



### 挖掘实验的结果



### 存在的问题



### 下一步工作

