from celery import Celery
from celery.schedules import crontab
from loguru import logger
import os

from app.core.config import settings


# 创建Celery实例
celery_app = Celery(
    "news_trending",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["tasks.api_tasks"]
)

# Celery配置
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    worker_hijack_root_logger=False,
)

# 定时任务配置
celery_app.conf.beat_schedule = {
    # 微博热搜
    "fetch_weibo_hourly": {
        "task": "tasks.api_tasks.fetch_weibo",
        "schedule": crontab(minute=0),  # 每小时整点
        "args": ()
    },
    # 百度热搜
    "fetch_baidu_hourly": {
        "task": "tasks.api_tasks.fetch_baidu",
        "schedule": crontab(minute=10),  # 每小时10分
        "args": ()
    },
    # 知乎热榜
    "fetch_zhihu_hourly": {
        "task": "tasks.api_tasks.fetch_zhihu",
        "schedule": crontab(minute=20),  # 每小时20分
        "args": ()
    },
    # 抖音热点
    "fetch_douyin_hourly": {
        "task": "tasks.api_tasks.fetch_douyin",
        "schedule": crontab(minute=30),  # 每小时30分
        "args": ()
    },
    # B站热门
    "fetch_bilibili_hourly": {
        "task": "tasks.api_tasks.fetch_bilibili",
        "schedule": crontab(minute=40),  # 每小时40分
        "args": ()
    },
    # 清理过期数据
    "clean_expired_data_daily": {
        "task": "tasks.api_tasks.clean_expired_data",
        "schedule": crontab(hour=3, minute=0),  # 每天凌晨3点
        "args": (settings.HISTORY_DAYS,)
    }
}


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    logger.info("设置定时任务...")
    for task_name, task_config in sender.conf.beat_schedule.items():
        logger.info(f"任务: {task_name}, 计划: {task_config['schedule']}")


if __name__ == "__main__":
    celery_app.start()