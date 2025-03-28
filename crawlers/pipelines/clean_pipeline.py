import re
from loguru import logger
from scrapy.exceptions import DropItem


class CleanPipeline:
    """数据清洗管道"""
    
    def process_item(self, item, spider):
        """处理爬虫项目，清洗数据"""
        # 检查必要字段
        required_fields = ['platform', 'title', 'url', 'rank']
        for field in required_fields:
            if not item.get(field):
                raise DropItem(f"缺少必要字段: {field}")
        
        # 清理标题
        title = item.get('title', '')
        if title:
            # 去除标题前后的空白字符
            title = title.strip()
            # 替换标题中的多个空白字符为单个空格
            title = re.sub(r'\s+', ' ', title)
            # 截断过长的标题
            if len(title) > 200:
                title = title[:197] + '...'
            
            if not title:  # 如果清理后标题为空，则丢弃该项
                raise DropItem("清理后标题为空，丢弃该项")
            
            item['title'] = title
        
        # 清理链接
        url = item.get('url', '')
        if url:
            # 去除URL前后的空白字符
            url = url.strip()
            
            if not url:  # 如果清理后URL为空，则丢弃该项
                raise DropItem("清理后URL为空，丢弃该项")
            
            item['url'] = url
        
        # 检查并转换排名
        rank = item.get('rank')
        if rank is not None:
            try:
                item['rank'] = int(rank)
            except (ValueError, TypeError):
                raise DropItem(f"排名不是有效的整数: {rank}")
        
        # 检查并转换热度值
        hot_value = item.get('hot_value')
        if hot_value is not None:
            try:
                item['hot_value'] = int(hot_value)
            except (ValueError, TypeError):
                logger.warning(f"热度值不是有效的整数，设为None: {hot_value}")
                item['hot_value'] = None
        
        # 清理内容
        content = item.get('content', '')
        if content:
            # 去除内容前后的空白字符
            content = content.strip()
            # 替换内容中的多个空白字符为单个空格
            content = re.sub(r'\s+', ' ', content)
            # 截断过长的内容
            if len(content) > 2000:
                content = content[:1997] + '...'
            
            item['content'] = content
        
        # 确保标签是列表
        tags = item.get('tags', [])
        if not isinstance(tags, list):
            item['tags'] = [str(tags)] if tags else []
        else:
            # 确保所有标签都是字符串
            item['tags'] = [str(tag) for tag in tags if tag]
        
        # 确保分类有值
        if not item.get('category'):
            item['category'] = 'general'
        
        logger.debug(f"数据清洗完成: [{item.get('platform')}] {item.get('title')}")
        return item 