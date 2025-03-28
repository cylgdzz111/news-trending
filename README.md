# AI热搜聚合平台

AI热搜聚合平台旨在通过人工智能技术自动收集、整合和分析各大互联网平台的热搜数据，为用户提供全面、实时、智能的热点资讯服务。

## 项目特点

- 覆盖5大热门平台：微博、百度、知乎、抖音、B站
- 每小时更新热搜数据
- 保留7天历史数据
- 按平台分类展示
- 提供基础筛选功能

## 技术栈

- **后端**：Python 3 + FastAPI
- **爬虫**：Scrapy + Selenium
- **数据库**：MongoDB + Redis
- **任务调度**：Celery
- **部署**：Docker

## 快速开始

### 使用Docker运行

```bash
# 克隆项目
git clone https://github.com/your-username/news-trending.git
cd news-trending

# 启动服务
docker-compose up -d

# 或手动启动各个组件
# 1. 启动API服务
uvicorn main:app --reload

# 2. 启动Celery Worker
celery -A tasks.celery_app worker --loglevel=info

# 3. 启动Celery Beat
celery -A tasks.celery_app beat --loglevel=info
```

服务启动后，访问API文档: http://localhost:8000/docs

### 手动安装运行

```bash
# 克隆项目
git clone https://github.com/your-username/news-trending.git
cd news-trending

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动API服务
uvicorn main:app --reload

# 启动Celery Worker
celery -A tasks.celery_app worker --loglevel=info

# 启动Celery Beat
celery -A tasks.celery_app beat --loglevel=info
```

## API文档

启动服务后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
/news-trending/
├── app/                      # 应用主目录
│   ├── api/                  # API服务
│   ├── core/                 # 核心配置
│   ├── db/                   # 数据库连接
│   ├── models/               # 数据模型
│   ├── schemas/              # 请求/响应模式
│   └── services/             # 业务逻辑服务
├── crawlers/                 # 爬虫模块
│   ├── spiders/              # 爬虫实现
│   ├── pipelines/            # 数据处理管道
│   └── middlewares/          # 爬虫中间件
├── tasks/                    # 后台任务
├── tests/                    # 测试代码
├── main.py                   # 应用入口
├── Dockerfile                # Docker配置
└── docker-compose.yml        # Docker编排
```

## 开发计划

- **版本1（基础版）**：覆盖5个平台，每小时更新，7天历史数据
- **版本2（成长版）**：增加5个平台，每30分钟更新，30天历史数据，热点聚合
- **版本3（高级版）**：增加5+，实时更新，180天历史数据，热点预测

## 贡献指南

欢迎提交Issue和Pull Request!