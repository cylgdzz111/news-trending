import scrapy
from datetime import datetime


class HotSearchItem(scrapy.Item):
    """热搜条目"""
    platform = scrapy.Field()  # 平台: weibo, baidu, zhihu, douyin, bilibili
    title = scrapy.Field()  # 热搜标题
    url = scrapy.Field()  # 热搜链接
    rank = scrapy.Field()  # 排名
    hot_value = scrapy.Field()  # 热度值
    category = scrapy.Field()  # 分类
    content = scrapy.Field()  # 相关内容
    tags = scrapy.Field()  # 标签
    created_at = scrapy.Field()  # 创建时间
    updated_at = scrapy.Field()  # 更新时间
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置默认值
        self.setdefault('category', 'general')
        self.setdefault('tags', [])
        self.setdefault('content', None)
        self.setdefault('hot_value', None)
        now = datetime.now()
        self.setdefault('created_at', now)
        self.setdefault('updated_at', now) 