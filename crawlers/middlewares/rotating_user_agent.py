import random
from scrapy import signals
from loguru import logger


class RotatingUserAgentMiddleware:
    """随机切换User Agent的中间件"""
    
    def __init__(self):
        self.user_agents = [
            # Chrome
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            # Firefox
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0',
            'Mozilla/5.0 (X11; Linux i686; rv:93.0) Gecko/20100101 Firefox/93.0',
            # Edge
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47',
            # Safari
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
            # Opera
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.63',
            # Mobile
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36'
        ]
    
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware
    
    def spider_opened(self, spider):
        user_agent = getattr(spider, 'user_agent', None)
        if not user_agent and hasattr(spider, 'custom_settings') and 'USER_AGENT' in spider.custom_settings:
            user_agent = spider.custom_settings['USER_AGENT']
        
        if user_agent:
            logger.info(f"Spider {spider.name} 使用自定义 User Agent: {user_agent}")
        else:
            logger.info(f"Spider {spider.name} 将使用随机 User Agent")
    
    def process_request(self, request, spider):
        user_agent = getattr(spider, 'user_agent', None)
        if not user_agent and hasattr(spider, 'custom_settings') and 'USER_AGENT' in spider.custom_settings:
            user_agent = spider.custom_settings['USER_AGENT']
        
        if not user_agent:  # 如果spider未设置 user_agent，则从列表中随机选择一个
            user_agent = random.choice(self.user_agents)
            logger.debug(f"使用随机 User Agent: {user_agent}")
        
        request.headers['User-Agent'] = user_agent 