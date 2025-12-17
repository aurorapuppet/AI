# 教材/课程 AI 检索问答平台

最小可行版 (MVP) 包含：
- 前端：Next.js + Tailwind（`/frontend`）
- 后端：FastAPI（`/backend`）
- 数据库：Postgres + PGVector（通过 Docker Compose）
- 本地/外部 LLM 集成接口（可切换供应商）

快速开始（本地开发）：

1. 克隆仓库并进入目录
2. 后端：
   - python -m venv .venv
   - source .venv/Scripts/activate  # Windows PowerShell: .\.venv\Scripts\Activate.ps1
   - pip install -r backend/requirements.txt
   - uvicorn app.main:app --reload --app-dir backend/app --port 8000
3. 前端：
   - cd frontend
   - yarn install
   - yarn dev

使用 Docker Compose：
  docker-compose up --build

下一步：实现文件上传与文本抽取。