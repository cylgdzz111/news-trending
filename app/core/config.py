from typing import List, Optional
from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    # 项目基本信息
    PROJECT_NAME: str = "AI热搜聚合平台"
    PROJECT_DESCRIPTION: str = "通过AI技术自动收集和分析各大平台热搜数据"
    PROJECT_VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # 跨域配置
    CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # 数据库配置
    MONGODB_URL: str = "mongodb://localhost:27017/news_trending"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Celery配置
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # 爬虫配置
    CRAWL_FREQUENCY: int = 60  # 爬取频率(分钟)
    HISTORY_DAYS: int = 7  # 历史数据保留天数
    
    # 平台配置
    PLATFORMS: List[str] = ["weibo", "baidu", "zhihu", "douyin", "bilibili"]
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings() 