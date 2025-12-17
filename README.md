# AI 智能问答平台

基于大语言模型的直接问答系统（无需上传教材）。

## 项目架构

**完整可用版本** 包含：
- **前端**：Next.js 13.4 + React 18.2 + Tailwind CSS 4.1 + Axios
- **后端**：FastAPI + SQLAlchemy + PostgreSQL 15
- **LLM 集成**：Alibaba Cloud (DashScope)、OpenAI、本地模型（可切换）
- **数据持久化**：问答记录存储、用户评分与反馈

## 核心功能

✅ **直接问答**：用户提问 → LLM 自动回答（无需检索文档）
✅ **答案评分**：1-5 星评分系统 + 反馈文本
✅ **历史记录**：自动保存所有问答对，支持分页查看
✅ **模型切换**：通过环境变量切换 LLM 提供商
✅ **错误处理**：完整的异常处理和用户提示

## 快速开始

### 🚀 一键启动（推荐）

```powershell
cd "d:\桌面\AI"
.\启动.ps1
```

### 📖 详细启动指南

选择以下任意一个文档开始：

| 启动方式 | 文档 | 适合场景 |
|---------|------|---------|
| **一键启动** | [TEST_AND_STARTUP_SUMMARY.md](TEST_AND_STARTUP_SUMMARY.md) | 快速上手 |
| **手动启动** | [MANUAL_STARTUP.md](MANUAL_STARTUP.md) | 开发调试 |
| **Docker** | [DOCKER_GUIDE.md](DOCKER_GUIDE.md) | 生产部署 |
| **详细测试** | [TESTING_GUIDE.md](TESTING_GUIDE.md) | 功能验证 |

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/Scripts/activate  # 或 venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --port 8000
```

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务
npm run dev
```

访问 `http://localhost:3000`

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/ask` | 提交问题，获取 LLM 答案 |
| GET | `/questions` | 获取历史问答记录（分页） |
| GET | `/questions/{id}` | 获取单个问答详情 |
| POST | `/questions/{id}/rate` | 评分与反馈 |
| DELETE | `/questions/{id}` | 删除记录 |
| GET | `/health` | 健康检查 |

## 项目结构

```
d:\桌面\AI\
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI 应用 (6 个端点)
│   │   ├── models.py        # SQLAlchemy 模型 (Question 表)
│   │   ├── llm.py           # LLM 多供应商支持
│   │   ├── rag.py           # 问答逻辑 (ask_direct)
│   │   ├── embedding.py     # 文本向量化
│   │   ├── db.py            # 数据库配置
│   │   └── extractors.py    # 文本提取 (预留)
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env
├── frontend/
│   ├── pages/
│   │   ├── _app.tsx
│   │   └── index.tsx                # 主页面（问答界面）
│   ├── components/
│   │   ├── QuestionForm.tsx         # 问题输入表单
│   │   ├── AnswerDisplay.tsx        # 答案显示与评分
│   │   └── HistoryList.tsx          # 历史记录列表
│   ├── lib/
│   │   └── api.ts                   # API 客户端
│   ├── styles/
│   │   └── globals.css
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── .env.local
│   └── FRONTEND_README.md
├── QUICK_START.md            # 详细启动指南
└── README.md                 # 本文件
```

## 完成的工作

### 后端（已完成）
- [x] FastAPI 应用框架与 6 个 REST 端点
- [x] SQLAlchemy ORM 与数据模型（Question 表）
- [x] 多供应商 LLM 抽象 (OpenAI, Alibaba, Local)
- [x] 问答逻辑与数据持久化
- [x] 文本向量化与相似度计算
- [x] 数据库初始化与连接池

### 前端（已完成）
- [x] Next.js 13 + React 项目初始化
- [x] Tailwind CSS 样式配置
- [x] API 客户端封装 (lib/api.ts)
- [x] QuestionForm 组件（问题输入）
- [x] AnswerDisplay 组件（答案展示 + 评分）
- [x] HistoryList 组件（历史记录）
- [x] 主页面整合（pages/index.tsx）
- [x] 状态管理与错误处理

## 功能特性

### 问题输入
- 大文本框，支持多行输入
- 自动禁用空白提交
- Loading 状态提示

### 答案显示
- 清晰的问答对展示
- 显示使用的 LLM 模型名称
- 文本保持格式（换行符）

### 评分系统
- 5 星评分界面（可视化星级）
- 反馈文本框（可选）
- 提交后重新加载历史记录

### 历史管理
- 列表展示所有问答
- 支持分页（上一页/下一页）
- 点击历史项查看详情
- 删除单条记录

## 环境配置

### 后端 (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/ai_qa
LLM_PROVIDER=alibaba
DASHSCOPE_API_KEY=your_key
```

### 前端 (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 部署选项

### Docker Compose
```bash
docker-compose up --build
```

### 云平台部署
- 前端：Vercel、Netlify
- 后端：AWS EC2、Azure App Service、Heroku

## 故障排除

**后端无法连接数据库**
```bash
docker run --name postgres -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:15
```

**前端无法访问后端**
- 检查 NEXT_PUBLIC_API_URL 配置
- 确保后端运行在 8000 端口

**LLM API 错误**
- 验证 API Key 有效性
- 检查网络连接和请求额度

## 下一步计划

1. **用户认证**：添加登录/注册功能
2. **数据导出**：支持问答记录 PDF/CSV 导出
3. **高级评估**：问答质量自动评分
4. **性能优化**：缓存、请求去重等
5. **移动适配**：响应式设计完善

## 许可证

MIT