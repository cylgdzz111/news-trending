import pymongo
from loguru import logger
from datetime import datetime

from scrapy.exceptions import DropItem
from pymongo.errors import DuplicateKeyError


class MongoPipeline:
    """MongoDB存储管道"""
    
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.client = None
        self.db = None
        self.collection = None
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DATABASE'),
            mongo_collection=crawler.settings.get('MONGODB_COLLECTION')
        )
    
    def open_spider(self, spider):
        """爬虫启动时，连接MongoDB"""
        logger.info(f"连接MongoDB: {self.mongo_uri}")
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]
        
        # 创建索引
        self.collection.create_index([("platform", pymongo.ASCENDING), ("title", pymongo.ASCENDING)], unique=True)
        self.collection.create_index("created_at", expireAfterSeconds=7 * 24 * 60 * 60)  # 7天后过期
        logger.info("MongoDB连接成功，索引已创建")
    
    def close_spider(self, spider):
        """爬虫关闭时，关闭MongoDB连接"""
        if self.client:
            self.client.close()
            logger.info("MongoDB连接已关闭")
    
    def process_item(self, item, spider):
        """处理并存储爬虫项目"""
        if not item.get('title'):
            raise DropItem("缺少标题，丢弃该项")
        
        now = datetime.now()
        data = dict(item)
        data['updated_at'] = now
        
        try:
            # 使用upsert模式，存在则更新，不存在则插入
            self.collection.update_one(
                {
                    "platform": data['platform'], 
                    "title": data['title']
                },
                {"$set": data},
                upsert=True
            )
            logger.debug(f"数据已存储: [{data['platform']}] {data['title']}")
        except DuplicateKeyError:
            logger.warning(f"重复数据: [{data['platform']}] {data['title']}")
        except Exception as e:
            logger.error(f"数据存储失败: {e}")
            raise DropItem(f"数据存储失败: {e}")
        
        return item 