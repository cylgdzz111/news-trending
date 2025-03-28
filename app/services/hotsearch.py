from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import DESCENDING

from app.models.hotsearch import HotSearchModel
from app.schemas.hotsearch import HotSearchCreate, HotSearchUpdate, HotSearchQueryParams


async def get_all_hotsearches(
    db: AsyncIOMotorClient,
    skip: int = 0,
    limit: int = 100
) -> List[dict]:
    """获取所有热搜"""
    hotsearches = []
    collection = db[HotSearchModel.Config.collection]
    
    cursor = collection.find().sort("created_at", DESCENDING).skip(skip).limit(limit)
    async for doc in cursor:
        hotsearches.append(doc)
        
    return hotsearches


async def get_hotsearches_by_platform(
    db: AsyncIOMotorClient,
    platform: str,
    skip: int = 0,
    limit: int = 100
) -> List[dict]:
    """按平台获取热搜"""
    hotsearches = []
    collection = db[HotSearchModel.Config.collection]
    
    cursor = collection.find({"platform": platform}).sort([
        ("created_at", DESCENDING),
        ("rank", 1)
    ]).skip(skip).limit(limit)
    
    async for doc in cursor:
        hotsearches.append(doc)
        
    return hotsearches


async def get_hotsearch(
    db: AsyncIOMotorClient,
    hotsearch_id: str
) -> Optional[dict]:
    """获取单个热搜"""
    collection = db[HotSearchModel.Config.collection]
    return await collection.find_one({"_id": hotsearch_id})


async def create_hotsearch(
    db: AsyncIOMotorClient,
    hotsearch: HotSearchCreate
) -> dict:
    """创建热搜"""
    collection = db[HotSearchModel.Config.collection]
    
    hotsearch_dict = hotsearch.dict()
    hotsearch_dict["created_at"] = datetime.now()
    hotsearch_dict["updated_at"] = datetime.now()
    
    result = await collection.insert_one(hotsearch_dict)
    
    return await collection.find_one({"_id": result.inserted_id})


async def update_hotsearch(
    db: AsyncIOMotorClient,
    hotsearch_id: str,
    hotsearch: HotSearchUpdate
) -> Optional[dict]:
    """更新热搜"""
    collection = db[HotSearchModel.Config.collection]
    
    hotsearch_dict = {k: v for k, v in hotsearch.dict().items() if v is not None}
    hotsearch_dict["updated_at"] = datetime.now()
    
    await collection.update_one(
        {"_id": hotsearch_id},
        {"$set": hotsearch_dict}
    )
    
    return await collection.find_one({"_id": hotsearch_id})


async def delete_hotsearch(
    db: AsyncIOMotorClient,
    hotsearch_id: str
) -> bool:
    """删除热搜"""
    collection = db[HotSearchModel.Config.collection]
    result = await collection.delete_one({"_id": hotsearch_id})
    return result.deleted_count > 0


async def search_hotsearches(
    db: AsyncIOMotorClient,
    params: HotSearchQueryParams
) -> List[dict]:
    """搜索热搜"""
    hotsearches = []
    collection = db[HotSearchModel.Config.collection]
    
    query: Dict[str, Any] = {}
    
    # 平台过滤
    if params.platform:
        query["platform"] = params.platform
    
    # 分类过滤
    if params.category:
        query["category"] = params.category
    
    # 日期过滤
    date_query = {}
    if params.start_date:
        date_query["$gte"] = params.start_date
    if params.end_date:
        date_query["$lte"] = params.end_date
    if date_query:
        query["created_at"] = date_query
    
    # 关键词过滤
    if params.keyword:
        query["$or"] = [
            {"title": {"$regex": params.keyword, "$options": "i"}},
            {"content": {"$regex": params.keyword, "$options": "i"}}
        ]
    
    cursor = collection.find(query).sort("created_at", DESCENDING).skip(params.skip).limit(params.limit)
    async for doc in cursor:
        hotsearches.append(doc)
        
    return hotsearches


async def clean_expired_data(
    db: AsyncIOMotorClient,
    days: int = 7
) -> int:
    """清理过期数据"""
    collection = db[HotSearchModel.Config.collection]
    expiry_date = datetime.now() - timedelta(days=days)
    
    result = await collection.delete_many({"created_at": {"$lt": expiry_date}})
    deleted_count = result.deleted_count
    
    logger.info(f"已清理 {deleted_count} 条过期热搜数据")
    return deleted_count 