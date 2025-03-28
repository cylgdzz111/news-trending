from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.apis.weibo import WeiboAPI
from loguru import logger
import asyncio

async def fetch_weibo_hot_search():
    """获取微博热搜"""
    # 1. 初始化API客户端
    api_client = WeiboAPI()
    
    # 连接数据库
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client.news_trending
    collection = db.hotsearch
    
    try:
        # 2. 获取数据
        items = await api_client.fetch_hot_search()
        if not items:
            logger.warning("未获取到微博热搜数据")
            return
        
        logger.info(f"获取到 {len(items)} 条微博热搜数据")
            
        # 3. 存储数据
        # 使用批量插入提高效率
        if len(items) > 0:
            result = await collection.insert_many(items)
            if result and result.inserted_ids:
                logger.info(f"成功存储 {len(result.inserted_ids)} 条微博热搜数据")
            else:
                logger.error("数据存储失败")
        else:
            logger.warning("没有数据需要存储")
            
    except Exception as e:
        logger.exception(f"获取微博热搜失败: {str(e)}")
        
    finally:
        await client.close()
        
# 提供同步接口用于Celery任务
def sync_fetch_weibo_hot_search():
    """同步接口：获取微博热搜"""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(fetch_weibo_hot_search()) 