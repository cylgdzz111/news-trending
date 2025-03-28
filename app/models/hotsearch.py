from typing import List, Optional, ClassVar
from datetime import datetime
from pydantic import Field, model_validator

from app.models.base import MongoBaseModel


class HotSearchModel(MongoBaseModel):
    """热搜数据模型"""
    platform: str = Field(..., description="平台: weibo, baidu, zhihu, douyin, bilibili")
    title: str = Field(..., description="热搜标题")
    url: str = Field(..., description="热搜链接")
    rank: int = Field(..., description="排名")
    hot_value: Optional[int] = Field(None, description="热度值")
    category: str = Field("general", description="分类")
    content: Optional[str] = Field(None, description="相关内容")
    tags: List[str] = Field(default_factory=list, description="标签")
    
    model_config = {
        "collection": "hot_searches",
        "json_schema_extra": {
            "example": {
                "platform": "weibo",
                "title": "2023世界杯",
                "url": "https://s.weibo.com/weibo?q=2023%E4%B8%96%E7%95%8C%E6%9D%AF",
                "rank": 1,
                "hot_value": 6542321,
                "category": "sports",
                "content": "2023世界杯相关热搜",
                "tags": ["体育", "足球", "世界杯"],
                "created_at": "2023-01-01T12:00:00",
                "updated_at": "2023-01-01T12:00:00"
            }
        }
    } 