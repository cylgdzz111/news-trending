import redis
from loguru import logger

from app.core.config import settings

class RedisClient:
    def __init__(self):
        self.client = None
        
    def connect(self):
        """连接到Redis"""
        try:
            self.client = redis.from_url(settings.REDIS_URL)
            logger.info("成功连接到Redis")
        except Exception as e:
            logger.error(f"Redis连接失败: {e}")
            raise
            
    def get_client(self):
        """获取Redis客户端"""
        if not self.client:
            self.connect()
        return self.client
        
    def close(self):
        """关闭Redis连接"""
        if self.client:
            logger.info("正在关闭Redis连接...")
            self.client.close()
            logger.info("Redis连接已关闭")


redis_client = RedisClient()


def get_redis():
    """获取Redis客户端依赖"""
    return redis_client.get_client() 