# ⚙️ 手动配置指南（完整清单）

**重要：** 大部分配置是可选的。系统默认使用本地模型，无需任何外部配置即可运行。

---

## 📋 配置需求矩阵

| 项目 | 是否必需 | 难度 | 时间 | 说明 |
|------|---------|------|------|------|
| **Python 3.8+** | ✅ 必需 | ⭐ 简单 | 5 分钟 | 已通过 `.\启动.ps1` 检查 |
| **Node.js 16+** | ✅ 必需 | ⭐ 简单 | 5 分钟 | 已通过 `.\启动.ps1` 检查 |
| **PostgreSQL** | ⚠️ 半必需 | ⭐⭐ 中等 | 10 分钟 | 可用 Docker 替代 |
| **OpenAI API Key** | ❌ 可选 | ⭐ 简单 | 5 分钟 | 提升答案质量 |
| **阿里云千问 API Key** | ❌ 可选 | ⭐⭐ 中等 | 10 分钟 | 提升答案质量 |

---

## 🔴 必需配置（必须做）

### 1️⃣ Python 3.8+ 环境

#### 检查是否已安装
```powershell
python --version
```

**预期输出：** `Python 3.8.x` 或更高

#### 如果未安装

**下载地址：** https://www.python.org/downloads/

**安装步骤：**
1. 访问官网
2. 点击 "Download Python 3.11" (或最新版本)
3. 下载 Windows installer
4. 运行安装器
5. ✅ **重要：勾选 "Add Python to PATH"**
6. 完成安装
7. 重启 PowerShell 并验证：`python --version`

**验证成功：** 显示版本号 ≥ 3.8

---

### 2️⃣ Node.js 16+ 环境

#### 检查是否已安装
```powershell
node --version
npm --version
```

**预期输出：**
```
v16.0.0 (或更高)
8.0.0 (或更高)
```

#### 如果未安装

**下载地址：** https://nodejs.org/

**安装步骤：**
1. 访问官网
2. 点击 "LTS" (推荐稳定版)
3. 下载 Windows installer
4. 运行安装器
5. 一直点 "Next"
6. 完成安装
7. 重启 PowerShell 并验证：`node --version` 和 `npm --version`

**验证成功：** 都显示合适的版本号

---

## 🟡 半必需配置（推荐做）

### 3️⃣ PostgreSQL 数据库

#### 方案 A：使用 Docker（推荐，最简单）✅

**前置条件：** 已安装 Docker Desktop

**一行命令启动：**
```powershell
docker run --name postgres_ai -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15
```

**验证：**
```powershell
docker ps
```

应该看到一个名为 `postgres_ai` 的容器运行中。

**优势：**
- ✅ 无需安装，即装即用
- ✅ 自动隔离环境
- ✅ 容易删除（`docker rm postgres_ai`）
- ✅ 跨平台一致

---

#### 方案 B：本地安装 PostgreSQL（较复杂）

**下载地址：** https://www.postgresql.org/download/windows/

**安装步骤：**
1. 下载 PostgreSQL 15 Windows installer
2. 运行安装器
3. 记住 **postgres 用户密码**（重要！）
4. 端口选择 5432（默认）
5. 完成安装
6. 验证：
   ```powershell
   psql --version
   ```

**验证成功：** 显示 PostgreSQL 版本号

**初始化数据库：**
```powershell
# 连接到默认 postgres 数据库
psql -U postgres

# 在 psql 提示符下，创建数据库
CREATE DATABASE ai_qa;
\q
```

---

#### 如何选择？

| 选项 | 安装时间 | 使用难度 | 卸载难度 | 推荐度 |
|------|---------|---------|---------|--------|
| **Docker** | 1 分钟 | ⭐ 简单 | ⭐ 简单 | ⭐⭐⭐⭐⭐ |
| **本地安装** | 10 分钟 | ⭐⭐ 中等 | ⭐⭐⭐ 困难 | ⭐⭐⭐ |

**建议：** 如果已有 Docker，用 Docker。如果电脑性能有限，用本地安装。

---

## 🟢 可选配置（增强功能）

### 4️⃣ OpenAI API（可选，推荐）

#### 优势
- ✅ 答案质量最好
- ✅ 速度快（5-10 秒）
- ✅ 功能最强大
- ❌ 需要付费（先免费 $5 额度）

#### 获取步骤

**第 1 步：创建 OpenAI 账号**

1. 访问：https://platform.openai.com/signup
2. 用 Google/Microsoft/Email 注册
3. 验证邮箱
4. 完成注册

**第 2 步：获取 API Key**

1. 登录：https://platform.openai.com/account/api-keys
2. 点击 "Create new secret key"
3. 复制 Key（**只显示一次，立即保存！**）
4. 格式：`sk-xxxxxxxxxxxxxxxxxxxxxx`

**第 3 步：配置环境变量**

编辑文件：`backend/.env`

```bash
# 改这一行
LLM_PROVIDER=openai

# 添加或取消注释这一行
OPENAI_API_KEY=sk-your-api-key-here
```

**第 4 步：重启后端**

停止后端后重新启动：
```powershell
cd backend
python -m uvicorn app.main:app --reload
```

**第 5 步：验证**

访问 http://localhost:3000，提交问题，应该快速获得答案。

#### 成本说明
- 新账号有 $5 免费额度（3 个月有效）
- 之后按量计费：`gpt-3.5-turbo` 约 $0.0005 per 1K tokens
- 一个典型问答对约消耗 500-1000 tokens，成本 < $0.001

---

### 5️⃣ 阿里云千问 API（可选）

#### 优势
- ✅ 支持中文优化
- ✅ 价格便宜
- ✅ 国内服务器快速

#### 获取步骤

**第 1 步：注册阿里云账号**

1. 访问：https://www.aliyun.com/
2. 点击 "免费注册"
3. 用手机号注册
4. 实名认证（需要身份证照片）
5. 完成注册

⏱️ **耗时：** 10-30 分钟（包括实名认证）

**第 2 步：开通 DashScope 服务**

1. 登录 https://dashscope.aliyun.com/
2. 点击 "开通服务"（如果首次访问）
3. 同意协议
4. 完成开通

**第 3 步：获取 API Key**

1. 在 DashScope 控制台
2. 点击左侧 "API-KEY"
3. 点击 "创建新的API-KEY"
4. 复制 Key（**只显示一次，立即保存！**）
5. 格式：`sk-xxxxxxxxxxxxxxxxxxxxxx`

**第 4 步：配置环境变量**

编辑文件：`backend/.env`

```bash
# 改这一行
LLM_PROVIDER=alibaba

# 添加或取消注释这一行
DASHSCOPE_API_KEY=sk-your-api-key-here
```

**第 5 步：重启后端**

```powershell
cd backend
python -m uvicorn app.main:app --reload
```

**第 6 步：验证**

访问 http://localhost:3000，提交问题，应该快速获得中文优化的答案。

#### 成本说明
- 新账号有免费额度（额度会定期补充）
- 按量计费：`qwen-turbo` 约 ¥0.002 per 1K tokens
- 一个典型问答对约消耗 500-1000 tokens，成本 < ¥0.001

---

## 🔵 不需要配置的东西

### ✅ 已内置，开箱即用

| 项目 | 说明 |
|------|------|
| **本地 LLM（GPT-2）** | 已包含，无需配置，默认使用 |
| **向量化模型** | sentence-transformers 已自动下载 |
| **前端框架** | Next.js 已配置，自动安装 |
| **后端框架** | FastAPI 已配置，自动安装 |
| **数据库 ORM** | SQLAlchemy 已配置，自动安装 |

---

## 🎯 配置优先级

### 🟢 第 1 优先级（立即做，启动前）

```powershell
# 1. 检查 Python
python --version

# 2. 检查 Node.js
node --version
npm --version

# 3. 启动 PostgreSQL（选择一个）
# 方案 A：Docker（推荐）
docker run --name postgres_ai -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# 或方案 B：本地安装（自行完成）
```

### 🟡 第 2 优先级（启动后，可选）

```powershell
# 4. 配置 OpenAI（可选，增强质量）
# 编辑 backend/.env
# 设置 LLM_PROVIDER=openai
# 设置 OPENAI_API_KEY=sk-xxx

# 5. 配置阿里云千问（可选，中文优化）
# 编辑 backend/.env
# 设置 LLM_PROVIDER=alibaba
# 设置 DASHSCOPE_API_KEY=sk-xxx
```

---

## 📝 配置检查清单

### 启动前检查

- [ ] Python 3.8+ 已安装
  ```powershell
  python --version
  ```

- [ ] Node.js 16+ 已安装
  ```powershell
  node --version
  ```

- [ ] npm 8+ 已安装
  ```powershell
  npm --version
  ```

- [ ] PostgreSQL 已运行（Docker 或本地）
  ```powershell
  # Docker 检查
  docker ps | grep postgres
  
  # 或本地检查
  psql --version
  ```

### 启动和验证

- [ ] 运行 `.\启动.ps1` 成功
- [ ] 后端在 8000 端口运行
- [ ] 前端在 3000 端口运行
- [ ] 浏览器访问 http://localhost:3000 成功

### 可选增强（启动后）

- [ ] OpenAI API Key 已获取（可选）
- [ ] 后端 `.env` 文件已更新（可选）
- [ ] 阿里云千问 API Key 已获取（可选）
- [ ] 后端已重启（如果更新了 `.env`）

---

## 🚨 常见配置问题

### 问题 1: Python 不存在

```powershell
# 错误提示
'python' is not recognized as an internal or external command
```

**解决：**
1. 重新安装 Python，**必须勾选 "Add Python to PATH"**
2. 重启 PowerShell（完全关闭再打开）
3. 重新验证：`python --version`

---

### 问题 2: PostgreSQL 连接失败

```
psycopg2.OperationalError: could not connect to server
```

**解决：**

**如果用 Docker：**
```powershell
# 检查容器是否运行
docker ps

# 如果没看到 postgres，重新启动
docker run --name postgres_ai -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# 检查容器日志
docker logs postgres_ai
```

**如果本地安装：**
1. 确保 PostgreSQL 服务已启动
2. 检查 `.env` 中的 DATABASE_URL：
   ```
   postgresql://postgres:password@localhost:5432/ai_qa
   ```
3. 确保密码正确

---

### 问题 3: OpenAI API Key 无效

```
openai.error.AuthenticationError: Invalid API key provided
```

**解决：**
1. 访问 https://platform.openai.com/account/api-keys
2. 检查 API Key 是否过期（旧 key 需要重新生成）
3. 重新复制最新的 Key
4. 更新 `.env` 文件
5. 重启后端

---

### 问题 4: 阿里云千问 API 响应慢

**可能原因：**
1. 网络连接问题
2. 阿里云服务器响应慢
3. API Key 额度已用尽

**解决：**
1. 检查网络连接
2. 访问 https://dashscope.aliyun.com/ 检查额度状态
3. 如果额度用尽，等待额度补充或充值

---

## 📊 配置对比

### 使用不同 LLM 的对比

| 特性 | 本地 GPT-2 | OpenAI | 阿里云千问 |
|------|-----------|--------|-----------|
| **需要 API Key** | ❌ 否 | ✅ 是 | ✅ 是 |
| **答案质量** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **响应速度** | 30-60 秒 | 5-10 秒 | 5-15 秒 |
| **成本** | 免费 | $0.0005/1K tokens | ¥0.002/1K tokens |
| **中文支持** | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **GPU 需求** | 中等 | 无 | 无 |
| **网络依赖** | ❌ 无 | ✅ 需要 | ✅ 需要 |

---

## 💾 环境配置文件说明

### 文件位置
```
backend/.env
```

### 完整配置模板

```bash
# ========== 数据库配置 ==========
# PostgreSQL 连接字符串
# 格式：postgresql://用户名:密码@主机:端口/数据库名

# 使用 Docker 的情况（推荐）
DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_qa

# 使用本地 PostgreSQL 的情况（需要修改密码）
# DATABASE_URL=postgresql://postgres:你的密码@localhost:5432/ai_qa

# ========== LLM 配置 ==========
# 选择一个 LLM 提供商：local / openai / alibaba
LLM_PROVIDER=local

# ========== OpenAI 配置（可选）==========
# 获取地址：https://platform.openai.com/api-keys
# 去掉下一行的 # 并填入你的 API Key
# OPENAI_API_KEY=sk-your-api-key-here

# ========== 阿里云千问配置（可选）==========
# 获取地址：https://dashscope.aliyun.com/
# 去掉下一行的 # 并填入你的 API Key
# DASHSCOPE_API_KEY=sk-your-api-key-here

# ========== 其他配置 ==========
# API 端口（可选，默认 8000）
# API_PORT=8000

# 日志级别（可选，默认 INFO）
# LOG_LEVEL=INFO
```

### 配置修改步骤

1. **打开文件：** `backend/.env`
2. **修改内容：** 取消注释（删除 #）并填入你的密钥
3. **保存文件：** Ctrl+S
4. **重启后端：** 停止 → 重新运行启动命令

---

## 🎬 快速配置清单（按顺序）

### 如果什么都没有（从零开始）

```powershell
# 1. 安装 Python 3.8+
# 访问 https://www.python.org/downloads/ 下载并安装
# ⚠️ 记得勾选 "Add Python to PATH"

# 2. 安装 Node.js 16+
# 访问 https://nodejs.org/ 下载并安装

# 3. 验证安装
python --version      # 应该 >= 3.8
node --version        # 应该 >= 16
npm --version         # 应该 >= 8

# 4. 安装 Docker（推荐用 Docker 的 PostgreSQL）
# 访问 https://www.docker.com/products/docker-desktop

# 5. 启动 PostgreSQL
docker run --name postgres_ai -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# 6. 验证 PostgreSQL
docker ps | grep postgres

# 7. 现在可以运行
cd "d:\桌面\AI"
.\启动.ps1
```

### 如果已有 Python 和 Node.js

```powershell
# 1. 只需启动 PostgreSQL
docker run --name postgres_ai -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# 2. 验证
docker ps

# 3. 启动系统
cd "d:\桌面\AI"
.\启动.ps1
```

### 如果想用增强的 LLM

```powershell
# 1. 获取 API Key
# OpenAI: https://platform.openai.com/api-keys
# 或阿里云: https://dashscope.aliyun.com/

# 2. 编辑 backend/.env
# 设置 LLM_PROVIDER=openai 或 alibaba
# 设置对应的 API Key

# 3. 重启后端
# Ctrl+C 停止 → 重新运行 python -m uvicorn...

# 4. 验证
# 提交问题，应该快速获得答案
```

---

## ✅ 最小配置（极速启动）

**最少需要做的事：**

1. ✅ 检查 Python 3.8+
2. ✅ 检查 Node.js 16+
3. ✅ 启动 Docker PostgreSQL（或本地安装）
4. ✅ 运行 `.\启动.ps1`

**预计时间：** 10 分钟

**预期结果：** 系统完全可用

---

## 🎯 推荐配置方案

### 方案 A：最简单（推荐新手）

```
✅ Python 3.8+
✅ Node.js 16+
✅ Docker PostgreSQL
❌ OpenAI API（使用本地模型）
❌ 阿里云 API（使用本地模型）

预计时间：15 分钟
功能完整：是
答案质量：中等
```

### 方案 B：推荐平衡（推荐大多数）

```
✅ Python 3.8+
✅ Node.js 16+
✅ Docker PostgreSQL
✅ OpenAI API（或阿里云）
❌ 两个都配置

预计时间：25 分钟
功能完整：是
答案质量：优秀
```

### 方案 C：完全配置（推荐专业人士）

```
✅ Python 3.8+
✅ Node.js 16+
✅ PostgreSQL 本地安装
✅ OpenAI API
✅ 阿里云 API

预计时间：1 小时
功能完整：是
答案质量：优秀
灵活性：最高
```

---

## 📞 配置问题快速查询

| 问题 | 快速解决 |
|------|--------|
| Python 找不到 | 重装 + 勾选 "Add to PATH" + 重启 Shell |
| Node 找不到 | 重装 + 重启 Shell |
| PostgreSQL 连接失败 | Docker 检查：`docker ps` / 本地检查服务状态 |
| API Key 无效 | 访问官网重新生成 Key |
| 答案生成慢 | 正常（本地 30-60 秒）/ 配置 OpenAI 快 10 倍 |

---

## 🎓 下一步

1. ✅ **按照上面的清单做** → 10-30 分钟
2. ✅ **运行 `.\启动.ps1`** → 自动启动所有服务
3. ✅ **访问 http://localhost:3000** → 开始使用
4. ✅ **可选：配置 OpenAI/阿里云** → 增强答案质量

---

**需要帮助？** 查看 [START_QUICK_REFERENCE.md](START_QUICK_REFERENCE.md) 或 [QUICK_START.md](QUICK_START.md)
