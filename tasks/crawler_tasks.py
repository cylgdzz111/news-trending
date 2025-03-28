import subprocess
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


def get_project_root():
    """获取项目根目录"""
    return Path(__file__).parent.parent


@celery_app.task(name="tasks.crawler_tasks.crawl_weibo")
def crawl_weibo():
    """爬取微博热搜"""
    try:
        logger.info("开始爬取微博热搜")
        root_dir = get_project_root()
        result = subprocess.run(
            ["scrapy", "crawl", "weibo"],
            cwd=root_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error(f"微博热搜爬取失败: {result.stderr}")
            return {"status": "error", "message": result.stderr}
        
        # 更新平台最后爬取时间
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_update_platform_last_crawl("weibo"))
        
        logger.info("微博热搜爬取完成")
        return {"status": "success", "message": "微博热搜爬取完成"}
    except Exception as e:
        logger.exception(f"微博热搜爬取异常: {e}")
        return {"status": "error", "message": str(e)}


@celery_app.task(name="tasks.crawler_tasks.crawl_baidu")
def crawl_baidu():
    """爬取百度热搜"""
    try:
        logger.info("开始爬取百度热搜")
        # TODO: 实现百度热搜爬虫
        logger.warning("百度热搜爬虫尚未实现")
        return {"status": "skipped", "message": "百度热搜爬虫尚未实现"}
    except Exception as e:
        logger.exception(f"百度热搜爬取异常: {e}")
        return {"status": "error", "message": str(e)}


@celery_app.task(name="tasks.crawler_tasks.crawl_zhihu")
def crawl_zhihu():
    """爬取知乎热榜"""
    try:
        logger.info("开始爬取知乎热榜")
        # TODO: 实现知乎热榜爬虫
        logger.warning("知乎热榜爬虫尚未实现")
        return {"status": "skipped", "message": "知乎热榜爬虫尚未实现"}
    except Exception as e:
        logger.exception(f"知乎热榜爬取异常: {e}")
        return {"status": "error", "message": str(e)}


@celery_app.task(name="tasks.crawler_tasks.crawl_douyin")
def crawl_douyin():
    """爬取抖音热点"""
    try:
        logger.info("开始爬取抖音热点")
        # TODO: 实现抖音热点爬虫
        logger.warning("抖音热点爬虫尚未实现")
        return {"status": "skipped", "message": "抖音热点爬虫尚未实现"}
    except Exception as e:
        logger.exception(f"抖音热点爬取异常: {e}")
        return {"status": "error", "message": str(e)}


@celery_app.task(name="tasks.crawler_tasks.crawl_bilibili")
def crawl_bilibili():
    """爬取B站热门"""
    try:
        logger.info("开始爬取B站热门")
        # TODO: 实现B站热门爬虫
        logger.warning("B站热门爬虫尚未实现")
        return {"status": "skipped", "message": "B站热门爬虫尚未实现"}
    except Exception as e:
        logger.exception(f"B站热门爬取异常: {e}")
        return {"status": "error", "message": str(e)}


@celery_app.task(name="tasks.crawler_tasks.clean_expired_data")
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


async def _update_platform_last_crawl(platform_name):
    """更新平台最后爬取时间"""
    try:
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        await update_last_crawl(client, platform_name)
    except Exception as e:
        logger.exception(f"更新平台[{platform_name}]最后爬取时间异常: {e}")


@celery_app.task(name="tasks.crawler_tasks.crawl_all")
def crawl_all():
    """爬取所有平台"""
    results = {}
    
    # 爬取各平台热搜
    results["weibo"] = crawl_weibo()
    results["baidu"] = crawl_baidu()
    results["zhihu"] = crawl_zhihu()
    results["douyin"] = crawl_douyin()
    results["bilibili"] = crawl_bilibili()
    
    return {
        "status": "completed", 
        "results": results
    } 