# 数据库模块说明文档

## 数据库架构

### 1. MongoDB

用于持久化存储热搜数据和平台信息。

#### 1.1 数据库设计
```
news_trending/              # 数据库名
├── hot_searches/          # 热搜集合
├── platforms/             # 平台信息集合
└── system_logs/          # 系统日志集合
```

#### 1.2 集合结构

##### hot_searches 集合
```javascript
{
    "_id": ObjectId,           // 文档ID
    "platform": String,        // 平台名称
    "title": String,          // 热搜标题
    "url": String,            // 热搜链接
    "rank": Number,           // 排名
    "hot_value": Number,      // 热度值
    "category": String,       // 分类
    "content": String,        // 相关内容
    "tags": [String],         // 标签列表
    "created_at": DateTime,   // 创建时间
    "updated_at": DateTime    // 更新时间
}
```

##### platforms 集合
```javascript
{
    "_id": ObjectId,           // 文档ID
    "name": String,           // 平台代码
    "display_name": String,   // 显示名称
    "base_url": String,       // 基础URL
    "logo": String,           // Logo URL
    "is_active": Boolean,     // 是否激活
    "crawl_frequency": Number, // 爬取频率(分钟)
    "last_crawl": DateTime,   // 上次爬取时间
    "created_at": DateTime,   // 创建时间
    "updated_at": DateTime    // 更新时间
}
```

#### 1.3 索引设计

```javascript
// hot_searches 集合索引
db.hot_searches.createIndex({ "platform": 1 })
db.hot_searches.createIndex({ "created_at": 1 })
db.hot_searches.createIndex({ "title": "text" })
db.hot_searches.createIndex({ "platform": 1, "created_at": -1 })

// platforms 集合索引
db.platforms.createIndex({ "name": 1 }, { unique: true })
db.platforms.createIndex({ "is_active": 1 })
```

### 2. Redis

用于缓存和任务队列管理。

#### 2.1 数据库规划
```
DB 0: 应用缓存
DB 1: Celery Broker
DB 2: Celery Result Backend
```

#### 2.2 键值设计

##### 应用缓存 (DB 0)
```
hot_search:{platform}:list     # 平台热搜列表缓存
hot_search:{platform}:detail   # 热搜详情缓存
platform:list                  # 平台列表缓存
```

##### Celery Broker (DB 1)
```
celery                        # Celery任务队列
celery-schedule              # Celery Beat调度信息
```

##### Celery Result Backend (DB 2)
```
celery-task-meta-{task_id}   # 任务结果
celery-task-meta-{task_id}-log  # 任务日志
```

## 数据流向

### 1. 写入流程

```mermaid
graph TD
    A[爬虫模块] -->|原始数据| B[数据清洗]
    B -->|清洗后数据| C[MongoDB]
    B -->|缓存更新| D[Redis]
    E[API写入] -->|新数据| C
    E -->|缓存更新| D
```

### 2. 读取流程

```mermaid
graph TD
    A[客户端请求] -->|查询| B{Redis缓存}
    B -->|命中| C[返回数据]
    B -->|未命中| D[MongoDB查询]
    D -->|查询结果| E[更新缓存]
    E --> C
```

## 缓存策略

### 1. 缓存配置

```python
REDIS_CONFIG = {
    'hot_search_expire': 3600,    # 热搜列表缓存1小时
    'platform_expire': 86400,     # 平台信息缓存1天
    'detail_expire': 1800         # 详情缓存30分钟
}
```

### 2. 缓存更新

```python
async def update_cache(platform: str, data: list):
    """更新平台热搜缓存"""
    key = f"hot_search:{platform}:list"
    await redis.set(key, json.dumps(data), ex=3600)
```

### 3. 缓存清理

```python
async def clear_platform_cache(platform: str):
    """清理平台相关缓存"""
    pattern = f"hot_search:{platform}:*"
    keys = await redis.keys(pattern)
    if keys:
        await redis.delete(*keys)
```

## 数据备份

### 1. MongoDB备份

```bash
# 全量备份
mongodump --uri="mongodb://user:pass@host:port/news_trending" --out=/backup/mongodb/

# 增量备份
mongodump --uri="mongodb://user:pass@host:port/news_trending" \
    --query='{"created_at":{"$gt":ISODate("2024-03-01")}}' \
    --out=/backup/mongodb/incremental/
```

### 2. Redis备份

```bash
# 自动备份配置
save 900 1        # 900秒内有1个更改
save 300 10       # 300秒内有10个更改
save 60 10000     # 60秒内有10000个更改

# 备份文件配置
dir /data/redis/backup
dbfilename dump.rdb
```

## 监控指标

### 1. MongoDB监控

1. **性能指标**
   - 查询响应时间
   - 连接数
   - 索引使用率

2. **存储指标**
   - 数据大小
   - 索引大小
   - 文档数量

### 2. Redis监控

1. **性能指标**
   - 命中率
   - 内存使用
   - QPS

2. **连接指标**
   - 连接数
   - 阻塞客户端
   - 复制延迟

## 优化策略

### 1. MongoDB优化

1. **查询优化**
   ```javascript
   // 使用投影
   db.hot_searches.find(
       { platform: "weibo" },
       { title: 1, rank: 1, hot_value: 1 }
   )

   // 使用聚合
   db.hot_searches.aggregate([
       { $match: { platform: "weibo" } },
       { $sort: { rank: 1 } },
       { $limit: 50 }
   ])
   ```

2. **索引优化**
   ```javascript
   // 复合索引
   db.hot_searches.createIndex(
       { platform: 1, created_at: -1, rank: 1 }
   )
   ```

### 2. Redis优化

1. **内存优化**
   ```python
   # 设置最大内存
   maxmemory 2gb
   maxmemory-policy allkeys-lru
   ```

2. **连接优化**
   ```python
   # 连接池配置
   REDIS_POOL_CONFIG = {
       'max_connections': 100,
       'max_idle': 20,
       'timeout': 30
   }
   ```

## 安全配置

### 1. MongoDB安全

```javascript
// 创建用户
db.createUser({
    user: "app_user",
    pwd: "secure_password",
    roles: [
        { role: "readWrite", db: "news_trending" }
    ]
})

// 启用认证
security:
    authorization: enabled
```

### 2. Redis安全

```bash
# Redis配置
requirepass "secure_password"
bind 127.0.0.1
protected-mode yes
``` 