from typing import List, Optional
from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings
import os
from pathlib import Path


# 获取项目根目录
def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


# 环境变量文件路径
env_path = get_project_root() / ".env"


class Settings(BaseSettings):
    # 项目基本信息
    PROJECT_NAME: str = "AI热搜聚合平台"
    PROJECT_DESCRIPTION: str = "通过AI技术自动收集和分析各大平台热搜数据"
    PROJECT_VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # 跨域配置
    CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # 数据库配置
    MONGODB_URL: str = Field(
        default="mongodb://localhost:27017/news_trending",
        description="MongoDB连接字符串"
    )
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis连接字符串"
    )
    
    # Celery配置
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/1",
        description="Celery Broker URL"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/2",
        description="Celery Result Backend URL"
    )
    
    # 数据采集配置
    FETCH_FREQUENCY: int = 60  # 获取数据频率(分钟)
    HISTORY_DAYS: int = 7  # 历史数据保留天数
    
    # 平台配置
    PLATFORMS: List[str] = ["weibo", "baidu", "zhihu", "douyin", "bilibili"]
    
    model_config = {
        "case_sensitive": True,
        "env_file": str(env_path),
        "env_file_encoding": "utf-8",
        "extra": "ignore"
    }


settings = Settings() 