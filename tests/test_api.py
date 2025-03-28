import asyncio
import pytest
import sys
from app.apis.weibo import WeiboAPI

async def test_weibo_api():
    """测试微博热搜API"""
    print("正在测试微博API...")
    api_client = WeiboAPI()
    results = await api_client.fetch_hot_search()
    
    # 验证返回结果是列表
    assert isinstance(results, list)
    
    # 如果成功获取，验证数据格式
    if results:
        print(f"获取到 {len(results)} 条微博热搜数据")
        for i, item in enumerate(results[:5]):  # 只打印前5条数据
            print(f"#{item['rank']} {item['title']} - 热度: {item['hot_value']}")
            
        # 详细验证第一条数据
        item = results[0]
        assert 'title' in item
        assert 'url' in item
        assert 'rank' in item
        assert 'hot_value' in item
        assert 'platform' in item
        assert 'created_at' in item
        
        # 验证具体字段
        assert isinstance(item['title'], str)
        assert isinstance(item['url'], str)
        assert isinstance(item['rank'], int)
        assert isinstance(item['hot_value'], int)
        assert item['platform'] == 'weibo'
    else:
        print("未获取到微博热搜数据")
        
if __name__ == '__main__':
    asyncio.run(test_weibo_api()) 