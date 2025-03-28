from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.hotsearch import HotSearchModel


# 请求模式
class HotSearchCreate(BaseModel):
    """创建热搜请求"""
    platform: str
    title: str
    url: str
    rank: int
    hot_value: Optional[int] = None
    category: str = "general"
    content: Optional[str] = None
    tags: List[str] = []


class HotSearchUpdate(BaseModel):
    """更新热搜请求"""
    title: Optional[str] = None
    url: Optional[str] = None
    rank: Optional[int] = None
    hot_value: Optional[int] = None
    category: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None


# 响应模式
class HotSearchResponse(BaseModel):
    """热搜响应"""
    id: str
    platform: str
    title: str
    url: str
    rank: int
    hot_value: Optional[int] = None
    category: str
    content: Optional[str] = None
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }


class HotSearchList(BaseModel):
    """热搜列表响应"""
    data: List[HotSearchResponse]
    total: int


# 查询参数
class HotSearchQueryParams(BaseModel):
    """热搜查询参数"""
    platform: Optional[str] = None
    category: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    keyword: Optional[str] = None
    skip: int = 0
    limit: int = 100 