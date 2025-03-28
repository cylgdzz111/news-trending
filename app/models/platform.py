from typing import Optional, ClassVar
from datetime import datetime
from pydantic import Field, model_validator

from app.models.base import MongoBaseModel


class PlatformModel(MongoBaseModel):
    """平台信息模型"""
    name: str = Field(..., description="平台代码: weibo, baidu, zhihu, douyin, bilibili")
    display_name: str = Field(..., description="平台显示名称: 微博, 百度, 知乎, 抖音, B站")
    base_url: str = Field(..., description="平台基础URL")
    logo: Optional[str] = Field(None, description="平台Logo")
    is_active: bool = Field(True, description="是否激活")
    crawl_frequency: int = Field(60, description="爬取频率(分钟)")
    last_crawl: Optional[datetime] = Field(None, description="上次爬取时间")
    
    model_config = {
        "collection": "platforms",
        "json_schema_extra": {
            "example": {
                "name": "weibo",
                "display_name": "微博",
                "base_url": "https://s.weibo.com/top/summary",
                "logo": "https://example.com/weibo-logo.png",
                "is_active": True,
                "crawl_frequency": 60,
                "last_crawl": "2023-01-01T12:00:00",
                "created_at": "2023-01-01T10:00:00",
                "updated_at": "2023-01-01T10:00:00"
            }
        }
    } 