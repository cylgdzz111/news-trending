from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.models.platform import PlatformModel


# 请求模式
class PlatformCreate(BaseModel):
    """创建平台请求"""
    name: str
    display_name: str
    base_url: str
    logo: Optional[str] = None
    is_active: bool = True
    crawl_frequency: int = 60


class PlatformUpdate(BaseModel):
    """更新平台请求"""
    display_name: Optional[str] = None
    base_url: Optional[str] = None
    logo: Optional[str] = None
    is_active: Optional[bool] = None
    crawl_frequency: Optional[int] = None
    last_crawl: Optional[datetime] = None


# 响应模式
class PlatformResponse(BaseModel):
    """平台响应"""
    id: str
    name: str
    display_name: str
    base_url: str
    logo: Optional[str] = None
    is_active: bool
    crawl_frequency: int
    last_crawl: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class PlatformList(BaseModel):
    """平台列表响应"""
    data: list[PlatformResponse]
    total: int 