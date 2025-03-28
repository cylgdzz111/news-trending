import sys
import os
from pathlib import Path
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

from tasks.celery_app import celery_app
from app.core.config import settings
from app.services.hotsearch import clean_expired_data
from app.services.platform import update_last_crawl
from tasks.fetch import sync_fetch_weibo_hot_search

def get_project_root():
    """获取项目根目录"""
    return Path(__file__).parent.parent


@celery_app.task(name="tasks.api_tasks.fetch_weibo")
def fetch_weibo():
    """获取微博热搜"""
    try:
        logger.info("开始获取微博热搜")
        
        # 调用同步接口
        sync_fetch_weibo_hot_search()
        
        # 更新平台最后获取时间
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_update_platform_last_fetch("weibo"))
        
        logger.info("微博热搜获取完成")
        return {"status": "success", "message": "微博热搜获取完成"}
    except Exception as e:
        logger.exception(f"微博热搜获取异常: {e}")
        return {"status": "error", "message": str(e)}


@celery_app.task(name="tasks.api_tasks.fetch_baidu")
def fetch_baidu():
    """获取百度热搜"""
    try:
        logger.info("开始获取百度热搜")
        # TODO: 实现百度热搜API
        logger.warning("百度热搜API尚未实现")
        return {"status": "skipped", "message": "百度热搜API尚未实现"}
    except Exception as e:
        logger.exception(f"百度热搜获取异常: {e}")
        return {"status": "error", "message": str(e)}


@celery_app.task(name="tasks.api_tasks.fetch_zhihu")
def fetch_zhihu():
    """获取知乎热榜"""
    try:
        logger.info("开始获取知乎热榜")
        # TODO: 实现知乎热榜API
        logger.warning("知乎热榜API尚未实现")
        return {"status": "skipped", "message": "知乎热榜API尚未实现"}
    except Exception as e:
        logger.exception(f"知乎热榜获取异常: {e}")
        return {"status": "error", "message": str(e)}


@celery_app.task(name="tasks.api_tasks.fetch_douyin")
def fetch_douyin():
    """获取抖音热点"""
    try:
        logger.info("开始获取抖音热点")
        # TODO: 实现抖音热点API
        logger.warning("抖音热点API尚未实现")
        return {"status": "skipped", "message": "抖音热点API尚未实现"}
    except Exception as e:
        logger.exception(f"抖音热点获取异常: {e}")
        return {"status": "error", "message": str(e)}


@celery_app.task(name="tasks.api_tasks.fetch_bilibili")
def fetch_bilibili():
    """获取B站热门"""
    try:
        logger.info("开始获取B站热门")
        # TODO: 实现B站热门API
        logger.warning("B站热门API尚未实现")
        return {"status": "skipped", "message": "B站热门API尚未实现"}
    except Exception as e:
        logger.exception(f"B站热门获取异常: {e}")
        return {"status": "error", "message": str(e)}


@celery_app.task(name="tasks.api_tasks.clean_expired_data")
def clean_expired_data_task(days=7):
    """清理过期数据"""
    try:
        logger.info(f"开始清理{days}天前的过期数据")
        loop = asyncio.get_event_loop()
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        result = loop.run_until_complete(clean_expired_data(client, days))
        logger.info(f"过期数据清理完成，共清理{result}条数据")
        return {"status": "success", "deleted_count": result}
    except Exception as e:
        logger.exception(f"过期数据清理异常: {e}")
        return {"status": "error", "message": str(e)}


async def _update_platform_last_fetch(platform_name):
    """更新平台最后获取时间"""
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        await update_last_crawl(client, platform_name)
    except Exception as e:
        logger.exception(f"更新平台[{platform_name}]最后获取时间异常: {e}")


@celery_app.task(name="tasks.api_tasks.fetch_all")
def fetch_all():
    """获取所有平台"""
    results = {}
    
    # 获取各平台热搜
    results["weibo"] = fetch_weibo()
    results["baidu"] = fetch_baidu()
    results["zhihu"] = fetch_zhihu()
    results["douyin"] = fetch_douyin()
    results["bilibili"] = fetch_bilibili()
    
    return {
        "status": "completed", 
        "results": results
    } 