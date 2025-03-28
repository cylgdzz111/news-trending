from urllib.parse import urlparse
from scrapy import signals
from loguru import logger


class ProxyMiddleware:
    """代理中间件"""
    
    def __init__(self, proxy_list=None):
        self.proxy_list = proxy_list or []
        self.proxy_index = 0
        self.enabled = len(self.proxy_list) > 0
    
    @classmethod
    def from_crawler(cls, crawler):
        # 从settings中获取代理列表
        proxy_list = crawler.settings.getlist('PROXY_LIST', [])
        
        middleware = cls(proxy_list)
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware
    
    def spider_opened(self, spider):
        if self.enabled:
            logger.info(f"Spider {spider.name} 启用代理中间件，代理列表: {self.proxy_list}")
        else:
            logger.info(f"Spider {spider.name} 未配置代理列表，代理中间件未启用")
    
    def process_request(self, request, spider):
        # 如果没有代理列表或者不启用代理，则直接返回
        if not self.enabled:
            return
        
        # 获取下一个代理
        proxy = self._get_next_proxy()
        if not proxy:
            return
        
        # 解析代理地址
        parsed = urlparse(proxy)
        scheme = parsed.scheme or 'http'
        
        # 为请求设置代理
        request.meta['proxy'] = f"{scheme}://{parsed.netloc}"
        logger.debug(f"为请求 {request.url} 设置代理: {request.meta['proxy']}")
        
        # 如果是HTTPS代理且需要认证
        if parsed.username and parsed.password:
            auth = f'{parsed.username}:{parsed.password}'
            request.headers['Proxy-Authorization'] = f'Basic {auth}'
    
    def _get_next_proxy(self):
        """获取下一个代理"""
        if not self.proxy_list:
            return None
        
        proxy = self.proxy_list[self.proxy_index]
        self.proxy_index = (self.proxy_index + 1) % len(self.proxy_list)
        return proxy 