import scrapy
from loguru import logger
from datetime import datetime

from crawlers.items import HotSearchItem


class WeiboSpider(scrapy.Spider):
    """微博热搜爬虫"""
    name = 'weibo'
    allowed_domains = ['s.weibo.com']
    start_urls = ['https://s.weibo.com/top/summary']
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    }
    
    def parse(self, response):
        """解析微博热搜榜页面"""
        if response.status != 200:
            logger.error(f"微博热搜页面请求失败: {response.status}")
            return
        
        logger.info("开始解析微博热搜榜...")
        hot_list = response.css('#pl_top_realtimehot table tbody tr')
        
        for idx, hot_item in enumerate(hot_list):
            rank_node = hot_item.css('.td-01::text').get()
            
            # 跳过标题行
            if not rank_node or not rank_node.strip().isdigit():
                continue
                
            rank = int(rank_node.strip())
            title_node = hot_item.css('.td-02 a::text').get()
            url_node = hot_item.css('.td-02 a::attr(href)').get()
            hot_node = hot_item.css('.td-02 span::text').get()
            
            if not title_node:
                continue
                
            title = title_node.strip()
            url = f"https://s.weibo.com{url_node}" if url_node else f"https://s.weibo.com/weibo?q={title}"
            
            # 提取热度值
            hot_value = None
            if hot_node:
                hot_text = hot_node.strip()
                if hot_text.isdigit():
                    hot_value = int(hot_text)
                else:
                    # 处理带单位的热度，如"12.3万"
                    hot_text = hot_text.rstrip("万")
                    try:
                        hot_value = int(float(hot_text) * 10000)
                    except (ValueError, TypeError):
                        pass
            
            # 判断是否置顶或推荐
            is_top = False
            is_recommend = False
            icon = hot_item.css('.td-03 i')
            if icon:
                icon_class = icon.attrib.get('class', '')
                is_top = 'top' in icon_class
                is_recommend = 'recommend' in icon_class
            
            # 确定分类
            category = 'general'
            if is_top:
                category = 'top'
            elif is_recommend:
                category = 'recommend'
            
            item = HotSearchItem(
                platform='weibo',
                title=title,
                url=url,
                rank=rank,
                hot_value=hot_value,
                category=category,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            yield item
            
        logger.info(f"微博热搜榜解析完成，共获取{len(hot_list)}条数据") 