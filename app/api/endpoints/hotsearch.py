from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path

from motor.motor_asyncio import AsyncIOMotorClient

from app.db.mongodb import get_database
from app.services import hotsearch
from app.schemas.hotsearch import (
    HotSearchResponse, 
    HotSearchList, 
    HotSearchCreate, 
    HotSearchUpdate,
    HotSearchQueryParams
)

router = APIRouter()


@router.get("/", response_model=HotSearchList)
async def read_hotsearches(
    db: AsyncIOMotorClient = Depends(get_database),
    skip: int = Query(0, description="跳过记录数"),
    limit: int = Query(100, description="返回记录数")
):
    """获取所有热搜"""
    hotsearches = await hotsearch.get_all_hotsearches(db, skip, limit)
    return {"data": hotsearches, "total": len(hotsearches)}


@router.get("/platform/{platform}", response_model=HotSearchList)
async def read_platform_hotsearches(
    platform: str = Path(..., description="平台标识: weibo, baidu, zhihu, douyin, bilibili"),
    db: AsyncIOMotorClient = Depends(get_database),
    skip: int = Query(0, description="跳过记录数"),
    limit: int = Query(100, description="返回记录数")
):
    """获取指定平台的热搜"""
    if platform not in ["weibo", "baidu", "zhihu", "douyin", "bilibili"]:
        raise HTTPException(status_code=400, detail="无效的平台标识")
    
    hotsearches = await hotsearch.get_hotsearches_by_platform(db, platform, skip, limit)
    return {"data": hotsearches, "total": len(hotsearches)}


@router.get("/{hotsearch_id}", response_model=HotSearchResponse)
async def read_hotsearch(
    hotsearch_id: str = Path(..., description="热搜ID"),
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取单个热搜"""
    db_hotsearch = await hotsearch.get_hotsearch(db, hotsearch_id)
    if db_hotsearch is None:
        raise HTTPException(status_code=404, detail="热搜数据不存在")
    return db_hotsearch


@router.post("/", response_model=HotSearchResponse)
async def create_hotsearch(
    hotsearch_data: HotSearchCreate,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """创建热搜"""
    return await hotsearch.create_hotsearch(db, hotsearch_data)


@router.put("/{hotsearch_id}", response_model=HotSearchResponse)
async def update_hotsearch(
    hotsearch_id: str,
    hotsearch_data: HotSearchUpdate,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """更新热搜"""
    db_hotsearch = await hotsearch.get_hotsearch(db, hotsearch_id)
    if db_hotsearch is None:
        raise HTTPException(status_code=404, detail="热搜数据不存在")
    
    return await hotsearch.update_hotsearch(db, hotsearch_id, hotsearch_data)


@router.delete("/{hotsearch_id}", response_model=dict)
async def delete_hotsearch(
    hotsearch_id: str,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """删除热搜"""
    db_hotsearch = await hotsearch.get_hotsearch(db, hotsearch_id)
    if db_hotsearch is None:
        raise HTTPException(status_code=404, detail="热搜数据不存在")
    
    success = await hotsearch.delete_hotsearch(db, hotsearch_id)
    return {"success": success}


@router.post("/search", response_model=HotSearchList)
async def search_hotsearches(
    params: HotSearchQueryParams,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """搜索热搜"""
    results = await hotsearch.search_hotsearches(db, params)
    return {"data": results, "total": len(results)} 