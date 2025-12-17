# 🐳 Docker 一键启动指南

完整的 Docker 部署方案，只需 Docker 和 Docker Compose。

## 前置条件

### 安装 Docker

**Windows:**
- 下载: https://www.docker.com/products/docker-desktop
- 安装 Docker Desktop
- 重启计算机

**验证安装：**
```powershell
docker --version
docker-compose --version
```

---

## 一键启动

### 方法 1: 使用 Docker Compose（推荐）

```powershell
cd "d:\桌面\AI"

# 启动所有服务
docker-compose up --build

# 成功标志：
# postgres-ai   | server started
# backend_ai    | INFO: Uvicorn running on http://0.0.0.0:8000
# frontend_ai   | ready - started server on 0.0.0.0:3000
```

打开浏览器：http://localhost:3000

### 方法 2: 单独启动服务

#### 启动 PostgreSQL

```powershell
docker run --name postgres-ai `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=password `
  -e POSTGRES_DB=ai_qa `
  -d `
  -p 5432:5432 `
  postgres:15

# 验证
docker ps
```

#### 启动后端

```powershell
cd "d:\桌面\AI\backend"

docker build -t backend-ai .

docker run --name backend-ai `
  --network host `
  -e DATABASE_URL="postgresql://postgres:password@localhost:5432/ai_qa" `
  -e LLM_PROVIDER=local `
  -d `
  -p 8000:8000 `
  backend-ai

# 验证
docker logs backend-ai
```

#### 启动前端

```powershell
cd "d:\桌面\AI\frontend"

docker build -t frontend-ai .

docker run --name frontend-ai `
  --network host `
  -e NEXT_PUBLIC_API_URL="http://localhost:8000" `
  -d `
  -p 3000:3000 `
  frontend-ai

# 验证
docker logs frontend-ai
```

---

## Docker Compose 文件更新

确保 `docker-compose.yml` 包含以下内容：

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:15
    container_name: postgres-ai
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: ai_qa
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d ai_qa"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: backend-ai
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/ai_qa
      LLM_PROVIDER: local
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: frontend-ai
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules

volumes:
  postgres_data:
```

---

## 常用 Docker 命令

### 查看运行的容器

```powershell
docker ps
docker ps -a  # 包括已停止的容器
```

### 查看日志

```powershell
# 后端日志
docker logs backend-ai

# 前端日志
docker logs frontend-ai

# 数据库日志
docker logs postgres-ai

# 实时日志
docker logs -f backend-ai
```

### 停止服务

```powershell
# 停止所有容器
docker-compose down

# 停止特定容器
docker stop backend-ai
docker stop frontend-ai
docker stop postgres-ai
```

### 删除容器和数据

```powershell
# 删除容器
docker-compose down

# 删除容器和数据卷
docker-compose down -v

# 删除镜像
docker rmi backend-ai
docker rmi frontend-ai
docker rmi postgres:15
```

### 进入容器

```powershell
# 进入后端容器
docker exec -it backend-ai bash

# 进入数据库容器
docker exec -it postgres-ai psql -U postgres -d ai_qa
```

---

## Dockerfile 配置

### 后端 Dockerfile

```dockerfile
# backend/Dockerfile

FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 前端 Dockerfile

```dockerfile
# frontend/Dockerfile

FROM node:18-alpine as builder

WORKDIR /app

# 安装依赖
COPY package*.json ./
RUN npm ci

# 复制代码
COPY . .

# 构建
RUN npm run build

# 生产镜像
FROM node:18-alpine

WORKDIR /app

# 只复制必要文件
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# 暴露端口
EXPOSE 3000

# 启动应用
CMD ["npm", "start"]
```

---

## Docker 网络连接

### 同一网络内部通信

当使用 Docker Compose 时，所有容器在同一网络中：

- 后端可以通过 `postgresql://postgres:5432/ai_qa` 连接数据库
- 前端通过 `http://backend:8000` 连接后端
- 但外部访问仍使用 `localhost`

### 跨容器通信示例

```yaml
# docker-compose.yml
services:
  backend:
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/ai_qa
```

---

## 生产部署建议

### 1. 多阶段构建
```dockerfile
# 减小镜像大小
FROM node:18 as builder
RUN npm ci && npm run build
FROM node:18-alpine
COPY --from=builder /app/.next ./.next
```

### 2. 健康检查
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### 3. 环境变量管理
```powershell
# 使用 .env 文件
docker-compose --env-file .env.production up
```

### 4. 日志管理
```yaml
logging:
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"
```

### 5. 资源限制
```yaml
resources:
  limits:
    cpus: "1"
    memory: 512M
  reservations:
    cpus: "0.5"
    memory: 256M
```

---

## 云平台部署

### AWS ECS

```bash
# 推送镜像到 ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
docker tag backend-ai <account>.dkr.ecr.<region>.amazonaws.com/backend:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/backend:latest
```

### Google Cloud Run

```bash
# 推送镜像到 GCR
gcloud builds submit --tag gcr.io/<project>/backend
gcloud run deploy backend --image gcr.io/<project>/backend --platform managed
```

### Azure Container Instances

```powershell
# 推送镜像
az acr build --registry <registry-name> --image backend:latest .

# 部署
az container create --resource-group <group> --name backend --image <registry>.azurecr.io/backend:latest
```

---

## 监控和日志

### 使用 Docker Stats

```powershell
docker stats

# 查看特定容器
docker stats backend-ai
```

### 使用 Docker Logs

```powershell
# 查看最后 100 行日志
docker logs --tail 100 backend-ai

# 实时日志
docker logs -f backend-ai
```

### 使用 ELK Stack (可选)

```yaml
version: '3.9'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"

  logstash:
    image: docker.elastic.co/logstash/logstash:8.0.0
    
  kibana:
    image: docker.elastic.co/kibana/kibana:8.0.0
    ports:
      - "5601:5601"
```

---

## 清理资源

```powershell
# 删除未使用的镜像
docker image prune

# 删除未使用的容器
docker container prune

# 删除未使用的卷
docker volume prune

# 完全清理（谨慎！）
docker system prune -a
```

---

## 检查清单

- [ ] Docker Desktop 已安装
- [ ] docker-compose.yml 正确配置
- [ ] Dockerfile 已创建
- [ ] 环境变量正确设置
- [ ] 容器可成功启动
- [ ] 健康检查通过
- [ ] 可从浏览器访问
- [ ] 日志正常输出
- [ ] 数据库连接成功

---

## 故障排除

### 容器无法启动

```powershell
# 查看错误日志
docker logs backend-ai

# 进入容器调试
docker run -it backend-ai bash
```

### 网络连接问题

```powershell
# 检查容器网络
docker inspect backend-ai | findstr "Networks" -A 10

# 测试容器间通信
docker exec backend-ai ping postgres
```

### 资源不足

```powershell
# 检查 Docker 资源使用
docker stats

# 清理未使用资源
docker system prune -a
```

---

**Docker 使用完全解决方案已准备就绪！**
