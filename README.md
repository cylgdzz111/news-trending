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
- **数据获取**：API接口 + aiohttp
- **数据库**：MongoDB + Redis
- **任务调度**：Celery
- **部署**：Docker

## 环境变量配置

本项目使用环境变量进行配置，以保护敏感信息。在开始使用前，请复制 `.env.example` 文件为 `.env`，并根据实际情况修改配置：

```bash
cp .env.example .env
```

重要的环境变量包括：

- `MONGODB_URL`：MongoDB连接字符串
- `REDIS_URL`：Redis连接字符串
- `CELERY_BROKER_URL`：Celery Broker URL
- `CELERY_RESULT_BACKEND`：Celery Result Backend URL

## 快速开始

### 本地使用pyenv运行（推荐）

```bash
# 1. 安装pyenv（如果没有安装）
brew install pyenv
brew install pyenv-virtualenv

# 2. 配置pyenv（如果是第一次使用）
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/shims ]] && export PATH="$PYENV_ROOT/shims:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
source ~/.zshrc

# 3. 克隆项目
git clone https://github.com/your-username/news-trending.git
cd news-trending

# 4. 安装Python并创建虚拟环境
pyenv install 3.11.7
pyenv virtualenv 3.11.7 news-trending-env
pyenv local news-trending-env

# 5. 安装依赖
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 6. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置你的数据库连接信息

# 7. 启动Redis（如果没有启动）
brew services start redis

# 8. 创建日志目录
mkdir -p logs

# 9. 启动服务（需要开启三个终端）

# 终端1：启动API服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 终端2：启动Celery Worker
celery -A tasks.celery_app worker --loglevel=info

# 终端3：启动Celery Beat
celery -A tasks.celery_app beat --loglevel=info
```

注意事项：
1. 确保在 `.env` 文件中正确设置 MongoDB 连接信息
2. 每次进入项目目录时，pyenv会自动激活对应的虚拟环境
3. 如果遇到MongoDB连接问题，请检查用户名密码和认证数据库配置

### 使用Docker运行

```bash
# 克隆项目
git clone https://github.com/your-username/news-trending.git
cd news-trending

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置你的数据库连接信息

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

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置你的数据库连接信息

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
│   ├── apis/                 # 第三方平台API客户端
│   ├── core/                 # 核心配置
│   ├── db/                   # 数据库连接
│   ├── models/               # 数据模型
│   ├── schemas/              # 请求/响应模式
│   └── services/             # 业务逻辑服务
├── tasks/                    # 后台任务
├── tests/                    # 测试代码
├── main.py                   # 应用入口
├── Dockerfile                # Docker配置
└── docker-compose.yml        # Docker编排
```

## 数据获取方式

本项目通过各平台的API接口获取热搜数据：

- 微博热搜：通过微博官方侧边栏API获取
- 百度热搜：API接口待实现
- 知乎热榜：API接口待实现
- 抖音热点：API接口待实现
- B站热门：API接口待实现

## 开发计划

- **版本1（基础版）**：覆盖5个平台，每小时更新，7天历史数据
- **版本2（成长版）**：增加5个平台，每30分钟更新，30天历史数据，热点聚合
- **版本3（高级版）**：增加5+，实时更新，180天历史数据，热点预测

## 贡献指南

欢迎提交Issue和Pull Request!