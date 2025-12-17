# AI 智能问答平台 - 快速开始指南

## 项目架构

- **前端**：Next.js + React + Tailwind CSS
- **后端**：FastAPI + SQLAlchemy + PostgreSQL
- **LLM**：支持 Alibaba Cloud (DashScope)、OpenAI、本地模型

## 完整启动步骤

### 1. 后端启动

#### a. 配置环境变量（backend/.env）

```bash
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/ai_qa

# LLM 配置（选择一个）
LLM_PROVIDER=alibaba  # 或 openai、local

# 如果使用阿里云
DASHSCOPE_API_KEY=your_alibaba_api_key

# 如果使用 OpenAI
OPENAI_API_KEY=your_openai_api_key
```

#### b. 安装依赖并启动

```bash
cd backend

# 创建虚拟环境（可选但推荐）
python -m venv venv
source venv/bin/activate  # 或 venv\Scripts\activate (Windows)

# 安装依赖
pip install -r requirements.txt

# 创建数据库表
python -c "from app.db import create_tables; create_tables()"

# 启动服务
uvicorn app.main:app --reload --port 8000
```

后端将在 `http://localhost:8000` 运行
API 文档访问 `http://localhost:8000/docs`

### 2. 前端启动

#### a. 配置环境变量（frontend/.env.local）

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### b. 安装依赖并启动

```bash
cd frontend

# 安装依赖
npm install

# 开发模式启动
npm run dev
```

前端将在 `http://localhost:3000` 运行

## 使用步骤

1. 打开浏览器访问 `http://localhost:3000`
2. 在文本框输入问题
3. 点击"获取答案"按钮
4. 等待 LLM 生成答案（取决于网络和 LLM 速度）
5. 查看答案，可以对答案进行评分和反馈
6. 在历史记录中查看之前的问题

## 关键 API 端点

| 方法 | 端点 | 功能 |
|------|------|------|
| POST | `/ask` | 提交问题并获取答案 |
| GET | `/questions` | 获取历史问题列表 |
| GET | `/questions/{id}` | 获取单个问题详情 |
| POST | `/questions/{id}/rate` | 对答案评分 |
| DELETE | `/questions/{id}` | 删除问题记录 |
| GET | `/health` | 健康检查 |

## 故障排除

### 1. 后端无法连接到数据库

**问题**：`could not translate host name "localhost" to address`

**解决**：
- 确保 PostgreSQL 服务运行
- 检查 DATABASE_URL 配置
- 可以使用 Docker 快速启动 PostgreSQL：

```bash
docker run --name postgres -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:15
```

然后更新 DATABASE_URL：`postgresql://postgres:password@localhost:5432/postgres`

### 2. 前端无法调用后端 API

**问题**：浏览器控制台报 CORS 或连接错误

**解决**：
- 检查后端是否运行在 8000 端口
- 检查 NEXT_PUBLIC_API_URL 环境变量
- 检查后端 CORS 配置（应已启用）

### 3. LLM API 错误

**问题**：`Invalid API Key` 或 `Rate limit exceeded`

**解决**：
- 检查 API Key 配置是否正确
- 确保 API Key 有足够额度
- 检查网络连接

### 4. npm 依赖错误

**问题**：`npm ERR! code ERESOLVE`

**解决**：
```bash
npm install --legacy-peer-deps
# 或
npm install --force
```

## 项目文件结构

```
d:\桌面\AI\
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI 应用主文件
│   │   ├── models.py            # SQLAlchemy 数据模型
│   │   ├── db.py                # 数据库配置
│   │   ├── llm.py               # LLM 提供商抽象
│   │   ├── rag.py               # 问答逻辑
│   │   ├── embedding.py         # 文本嵌入
│   │   └── extractors.py        # 文本提取（未使用）
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env
├── frontend/
│   ├── pages/
│   │   ├── _app.tsx             # Next.js 应用包装
│   │   └── index.tsx            # 主页面
│   ├── components/
│   │   ├── QuestionForm.tsx      # 问题输入表单
│   │   ├── AnswerDisplay.tsx     # 答案展示与评分
│   │   └── HistoryList.tsx       # 历史记录列表
│   ├── lib/
│   │   └── api.ts               # API 客户端
│   ├── styles/
│   │   └── globals.css          # 全局样式
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── next.config.js
│   ├── .env.local
│   └── FRONTEND_README.md
└── README.md
```

## 下一步

1. **自定义样式**：编辑 `tailwind.config.js` 或 `globals.css`
2. **添加功能**：如用户认证、分享、导出等
3. **性能优化**：添加缓存、请求防抖等
4. **部署**：使用 Docker Compose 或云平台部署

## 许可证

MIT
