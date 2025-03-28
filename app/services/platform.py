from typing import List, Optional
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING

from app.models.platform import PlatformModel
from app.schemas.platform import PlatformCreate, PlatformUpdate


async def get_all_platforms(
    db: AsyncIOMotorClient,
    skip: int = 0,
    limit: int = 100
) -> List[dict]:
    """获取所有平台"""
    platforms = []
    collection = db[PlatformModel.Config.collection]
    
    cursor = collection.find().sort("name", ASCENDING).skip(skip).limit(limit)
    async for doc in cursor:
        platforms.append(doc)
        
    return platforms


async def get_platform(
    db: AsyncIOMotorClient,
    platform_id: str = None,
    platform_name: str = None
) -> Optional[dict]:
    """获取单个平台"""
    collection = db[PlatformModel.Config.collection]
    
    if platform_id:
        return await collection.find_one({"_id": platform_id})
    elif platform_name:
        return await collection.find_one({"name": platform_name})
    
    return None


async def create_platform(
    db: AsyncIOMotorClient,
    platform: PlatformCreate
) -> dict:
    """创建平台"""
    collection = db[PlatformModel.Config.collection]
    
    # 检查平台是否已存在
    existing = await collection.find_one({"name": platform.name})
    if existing:
        return existing
    
    platform_dict = platform.dict()
    platform_dict["created_at"] = datetime.now()
    platform_dict["updated_at"] = datetime.now()
    
    result = await collection.insert_one(platform_dict)
    
    return await collection.find_one({"_id": result.inserted_id})


async def update_platform(
    db: AsyncIOMotorClient,
    platform_id: str,
    platform: PlatformUpdate
) -> Optional[dict]:
    """更新平台"""
    collection = db[PlatformModel.Config.collection]
    
    platform_dict = {k: v for k, v in platform.dict().items() if v is not None}
    platform_dict["updated_at"] = datetime.now()
    
    await collection.update_one(
        {"_id": platform_id},
        {"$set": platform_dict}
    )
    
    return await collection.find_one({"_id": platform_id})


async def delete_platform(
    db: AsyncIOMotorClient,
    platform_id: str
) -> bool:
    """删除平台"""
    collection = db[PlatformModel.Config.collection]
    result = await collection.delete_one({"_id": platform_id})
    return result.deleted_count > 0


async def update_last_crawl(
    db: AsyncIOMotorClient,
    platform_name: str
) -> Optional[dict]:
    """更新平台最后爬取时间"""
    collection = db[PlatformModel.Config.collection]
    
    now = datetime.now()
    await collection.update_one(
        {"name": platform_name},
        {"$set": {"last_crawl": now, "updated_at": now}}
    )
    
    return await collection.find_one({"name": platform_name})


async def get_active_platforms(
    db: AsyncIOMotorClient
) -> List[dict]:
    """获取所有激活的平台"""
    platforms = []
    collection = db[PlatformModel.Config.collection]
    
    cursor = collection.find({"is_active": True}).sort("name", ASCENDING)
    async for doc in cursor:
        platforms.append(doc)
        
    return platforms


async def initialize_default_platforms(
    db: AsyncIOMotorClient
) -> List[dict]:
    """初始化默认平台数据"""
    default_platforms = [
        {
            "name": "weibo",
            "display_name": "微博",
            "base_url": "https://s.weibo.com/top/summary",
            "is_active": True,
            "crawl_frequency": 60
        },
        {
            "name": "baidu",
            "display_name": "百度",
            "base_url": "https://top.baidu.com/board?tab=realtime",
            "is_active": True,
            "crawl_frequency": 60
        },
        {
            "name": "zhihu",
            "display_name": "知乎",
            "base_url": "https://www.zhihu.com/hot",
            "is_active": True,
            "crawl_frequency": 60
        },
        {
            "name": "douyin",
            "display_name": "抖音",
            "base_url": "https://www.douyin.com/hot",
            "is_active": True,
            "crawl_frequency": 60
        },
        {
            "name": "bilibili",
            "display_name": "B站",
            "base_url": "https://www.bilibili.com/v/popular/rank/all",
            "is_active": True,
            "crawl_frequency": 60
        }
    ]
    
    collection = db[PlatformModel.Config.collection]
    platforms = []
    
    for platform_data in default_platforms:
        # 检查平台是否已存在
        existing = await collection.find_one({"name": platform_data["name"]})
        if not existing:
            platform_data["created_at"] = datetime.now()
            platform_data["updated_at"] = datetime.now()
            await collection.insert_one(platform_data)
            platforms.append(platform_data)
        else:
            platforms.append(existing)
    
    return platforms 