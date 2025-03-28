from fastapi import APIRouter, Depends, HTTPException, Query, Path
from motor.motor_asyncio import AsyncIOMotorClient

from app.db.mongodb import get_database
from app.services import platform
from app.schemas.platform import (
    PlatformResponse, 
    PlatformList, 
    PlatformCreate, 
    PlatformUpdate
)

router = APIRouter()


@router.get("/", response_model=PlatformList)
async def read_platforms(
    db: AsyncIOMotorClient = Depends(get_database),
    skip: int = Query(0, description="跳过记录数"),
    limit: int = Query(100, description="返回记录数")
):
    """获取所有平台"""
    platforms = await platform.get_all_platforms(db, skip, limit)
    return {"data": platforms, "total": len(platforms)}


@router.get("/active", response_model=PlatformList)
async def read_active_platforms(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取所有激活的平台"""
    platforms = await platform.get_active_platforms(db)
    return {"data": platforms, "total": len(platforms)}


@router.get("/{platform_id}", response_model=PlatformResponse)
async def read_platform(
    platform_id: str = Path(..., description="平台ID"),
    db: AsyncIOMotorClient = Depends(get_database)
):
    """获取单个平台"""
    db_platform = await platform.get_platform(db, platform_id=platform_id)
    if db_platform is None:
        raise HTTPException(status_code=404, detail="平台不存在")
    return db_platform


@router.get("/name/{platform_name}", response_model=PlatformResponse)
async def read_platform_by_name(
    platform_name: str = Path(..., description="平台名称"),
    db: AsyncIOMotorClient = Depends(get_database)
):
    """通过名称获取平台"""
    db_platform = await platform.get_platform(db, platform_name=platform_name)
    if db_platform is None:
        raise HTTPException(status_code=404, detail="平台不存在")
    return db_platform


@router.post("/", response_model=PlatformResponse)
async def create_platform(
    platform_data: PlatformCreate,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """创建平台"""
    return await platform.create_platform(db, platform_data)


@router.put("/{platform_id}", response_model=PlatformResponse)
async def update_platform(
    platform_id: str,
    platform_data: PlatformUpdate,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """更新平台"""
    db_platform = await platform.get_platform(db, platform_id=platform_id)
    if db_platform is None:
        raise HTTPException(status_code=404, detail="平台不存在")
    
    return await platform.update_platform(db, platform_id, platform_data)


@router.delete("/{platform_id}", response_model=dict)
async def delete_platform(
    platform_id: str,
    db: AsyncIOMotorClient = Depends(get_database)
):
    """删除平台"""
    db_platform = await platform.get_platform(db, platform_id=platform_id)
    if db_platform is None:
        raise HTTPException(status_code=404, detail="平台不存在")
    
    success = await platform.delete_platform(db, platform_id)
    return {"success": success}


@router.post("/initialize", response_model=PlatformList)
async def initialize_platforms(
    db: AsyncIOMotorClient = Depends(get_database)
):
    """初始化默认平台"""
    platforms = await platform.initialize_default_platforms(db)
    return {"data": platforms, "total": len(platforms)}