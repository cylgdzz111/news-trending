# Scrapy设置文件

BOT_NAME = 'news_trending'

SPIDER_MODULES = ['crawlers.spiders']
NEWSPIDER_MODULE = 'crawlers.spiders'

# 请求头设置
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'

# 请求延迟
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True

# 并发请求数
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# 禁用cookies
COOKIES_ENABLED = False

# 启用的中间件
DOWNLOADER_MIDDLEWARES = {
    'crawlers.middlewares.rotating_user_agent.RotatingUserAgentMiddleware': 400,
    'crawlers.middlewares.proxy.ProxyMiddleware': 410,
}

# 启用的管道
ITEM_PIPELINES = {
    'crawlers.pipelines.clean_pipeline.CleanPipeline': 300,
    'crawlers.pipelines.mongo_pipeline.MongoPipeline': 800,
}

# 遵循robots.txt规则
ROBOTSTXT_OBEY = False

# 超时设置
DOWNLOAD_TIMEOUT = 30

# 重试设置
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# 日志设置
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/scrapy.log'

# MongoDB设置
MONGODB_URI = 'mongodb://localhost:27017/'
MONGODB_DATABASE = 'news_trending'
MONGODB_COLLECTION = 'hot_searches' 