import asyncio
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from loguru import logger

from app.core.config import settings

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    
    def get_client(self) -> AsyncIOMotorClient:
        """获取MongoDB客户端连接"""
        return self.client
    
    def get_database(self):
        """获取数据库"""
        return self.client.get_database()
    
    def get_collection(self, name: str):
        """获取集合"""
        return self.get_database()[name]


mongodb = MongoDB()


async def connect_to_mongo():
    """连接到MongoDB"""
    logger.info("正在连接到MongoDB...")
    
    try:
        mongodb.client = AsyncIOMotorClient(settings.MONGODB_URL)
        # 验证连接
        await mongodb.client.server_info()
        logger.info("成功连接到MongoDB")
    except Exception as e:
        logger.error(f"MongoDB连接失败: {e}")
        raise


async def close_mongo_connection():
    """关闭MongoDB连接"""
    if mongodb.client:
        logger.info("正在关闭MongoDB连接...")
        mongodb.client.close()
        logger.info("MongoDB连接已关闭")


def get_database():
    """获取数据库连接依赖"""
    return mongodb.get_database()


def get_collection(name: str):
    """获取指定集合依赖"""
    return mongodb.get_collection(name) 