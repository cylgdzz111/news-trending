from typing import List, Dict, Any
import aiohttp
from datetime import datetime
import logging

class WeiboAPI:
    """微博热搜API客户端"""
    
    def __init__(self):
        self.api_url = "https://weibo.com/ajax/side/hotSearch"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://weibo.com/",
        }
        self.logger = logging.getLogger("weibo_api")
    
    async def fetch_hot_search(self) -> List[Dict[str, Any]]:
        """
        获取微博热搜
        :return: 热搜数据列表
        """
        try:
            self.logger.info("正在请求微博热搜API...")
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_url, headers=self.headers) as response:
                    if response.status != 200:
                        self.logger.error(f"API请求失败: HTTP {response.status}")
                        return []
                    
                    data = await response.json()
                    self.logger.info("成功获取API响应")
                    
                    items = []
                    try:
                        # 解析API返回的数据格式
                        realtime_list = data.get("data", {}).get("realtime", [])
                        
                        for rank, item in enumerate(realtime_list, 1):
                            if not isinstance(item, dict):
                                continue
                                
                            title = item.get("word", "")
                            hot_value = item.get("num", 0)
                            url = f"https://s.weibo.com/weibo?q={title}"
                            
                            items.append({
                                "platform": "weibo",
                                "title": title,
                                "url": url,
                                "rank": rank,
                                "hot_value": int(hot_value) if hot_value else 0,
                                "category": "general",
                                "tags": [],
                                "created_at": datetime.now().isoformat(),
                                "updated_at": datetime.now().isoformat()
                            })
                        
                        self.logger.info(f"成功提取到 {len(items)} 条热搜数据")
                    except Exception as e:
                        self.logger.error(f"解析API数据失败: {str(e)}")
                        
                    return items
                    
        except Exception as e:
            self.logger.error(f"获取微博热搜失败: {str(e)}")
            return [] 