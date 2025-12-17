# ⚡ 配置速查表 (Quick Config Checklist)

**打印这个页面！** 最常用的配置说明

---

## 🎯 你现在需要什么？

### 情况 1: "我什么都没装，从零开始"

```
需要下载：
☐ Python 3.8+ (https://www.python.org/downloads/)
☐ Node.js 16+ (https://nodejs.org/)
☐ Docker Desktop (https://www.docker.com/products/docker-desktop)

需要做：
☐ 安装 Python，勾选 "Add Python to PATH"
☐ 安装 Node.js，默认安装即可
☐ 安装 Docker，默认安装即可
☐ 重启电脑

然后：
☐ 运行: docker run --name postgres_ai -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15
☐ 运行: cd "d:\桌面\AI" && .\启动.ps1

预计时间：1 小时
```

---

### 情况 2: "我已装了 Python 和 Node.js，缺数据库"

```
需要做：
☐ 安装 Docker
☐ 启动 PostgreSQL:
   docker run --name postgres_ai -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

然后：
☐ 运行: cd "d:\桌面\AI" && .\启动.ps1

预计时间：15 分钟
```

---

### 情况 3: "我想要更好的答案（快 10 倍）"

```
选择一个：

A. OpenAI（更好，$0.0005 per 1K tokens）
   ☐ 访问: https://platform.openai.com/signup
   ☐ 注册账号
   ☐ 访问: https://platform.openai.com/api-keys
   ☐ 点击 "Create new secret key"
   ☐ 复制 Key: sk-xxxxx

B. 阿里云千问（中文好，¥0.002 per 1K tokens）
   ☐ 访问: https://www.aliyun.com/
   ☐ 注册账号 + 实名认证
   ☐ 访问: https://dashscope.aliyun.com/
   ☐ 开通服务
   ☐ 点击 "API-KEY" → "创建新的API-KEY"
   ☐ 复制 Key: sk-xxxxx

然后编辑 backend/.env：
   LLM_PROVIDER=openai (或 alibaba)
   OPENAI_API_KEY=sk-xxxxx
   (或 DASHSCOPE_API_KEY=sk-xxxxx)

重启后端即可

预计时间：10-30 分钟
```

---

## 📥 详细下载链接

### Python 3.8+
```
官网: https://www.python.org/downloads/
推荐: Python 3.11 最新版
下载后: 勾选 "Add Python to PATH"
验证: python --version
```

### Node.js 16+
```
官网: https://nodejs.org/
推荐: LTS 版本（左边大按钮）
下载后: 默认安装即可
验证: node --version 和 npm --version
```

### Docker Desktop
```
官网: https://www.docker.com/products/docker-desktop/
选择: Windows 版本
下载后: 默认安装即可
验证: docker --version
```

### PostgreSQL（可选，不推荐）
```
官网: https://www.postgresql.org/download/windows/
建议: 改用 Docker (更简单)
如果要装: 记住 postgres 用户密码
```

---

## ⚙️ 配置 API Key

### 获取 OpenAI API Key

```
1. 访问: https://platform.openai.com/signup
2. 用邮箱/Google/Microsoft 账号注册
3. 验证邮箱
4. 访问: https://platform.openai.com/api-keys
5. 点击: "Create new secret key"
6. 复制: sk-xxxxxxxxxxxxxxxxx
7. 编辑: backend/.env

   改这一行:
   LLM_PROVIDER=openai
   
   加这一行:
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxx

8. 重启后端

时间: 10 分钟
成本: $5 免费额度（新注册）
```

---

### 获取阿里云千问 API Key

```
1. 访问: https://www.aliyun.com/
2. 点击 "免费注册"
3. 用手机号注册
4. 实名认证（拍身份证照片）
5. 访问: https://dashscope.aliyun.com/
6. 点击 "开通服务"
7. 左侧 "API-KEY" → "创建新的API-KEY"
8. 复制: sk-xxxxxxxxxxxxxxxxx
9. 编辑: backend/.env

   改这一行:
   LLM_PROVIDER=alibaba
   
   加这一行:
   DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxxx

10. 重启后端

时间: 20-30 分钟（包括实名认证）
成本: 有免费额度，按量计费
```

---

## 🗂️ 配置文件位置

### 后端配置
```
位置: d:\桌面\AI\backend\.env

编辑这部分:

LLM_PROVIDER=local  ← 改成 openai 或 alibaba
OPENAI_API_KEY=     ← 粘贴你的 OpenAI Key（如果用）
DASHSCOPE_API_KEY=  ← 粘贴你的阿里云 Key（如果用）
```

### 前端配置
```
位置: d:\桌面\AI\frontend\.env.local

一般不需要改，默认:
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🔄 启动数据库

### 方法 1: Docker（推荐，最简单）

```powershell
docker run --name postgres_ai -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# 验证
docker ps | grep postgres

# 停止
docker stop postgres_ai

# 删除
docker rm postgres_ai
```

### 方法 2: 本地 PostgreSQL（如果已装）

```powershell
# Windows 上 PostgreSQL 通常自动作为服务运行
# 验证:
psql --version

# 如果没运行，手动启动 PostgreSQL 服务
```

---

## 🧪 验证配置

### 检查清单

```powershell
# 1. 检查 Python
python --version
# 预期: Python 3.8.x 或更高

# 2. 检查 Node.js
node --version
# 预期: v16.0.0 或更高

# 3. 检查 npm
npm --version
# 预期: 8.0.0 或更高

# 4. 检查 Docker（如果用 Docker）
docker --version
# 预期: Docker version 19.03 或更高

# 5. 检查 PostgreSQL 运行
docker ps | grep postgres
# 或
psql --version

# 6. 检查后端配置
type backend\.env
# 应该看到配置内容
```

所有都 ✅ 就可以启动了！

---

## 🚀 最少配置（5 分钟快速方案）

```
假设已有 Python 3.8+ 和 Node.js 16+

1. 启动数据库:
   docker run --name postgres_ai -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

2. 启动系统:
   cd "d:\桌面\AI"
   .\启动.ps1

3. 访问:
   http://localhost:3000

完成！系统已可用。
答案质量中等（使用本地 GPT-2）。
```

---

## 📊 配置需求矩阵（一看就懂）

| 需要 | 必需? | 难度 | 时间 | 怎么做 |
|------|-------|------|------|--------|
| Python 3.8+ | ✅ 是 | ⭐ | 5 分钟 | 官网下载 + 勾选 Path |
| Node.js 16+ | ✅ 是 | ⭐ | 5 分钟 | 官网下载 + 默认安装 |
| PostgreSQL | ⚠️ 是* | ⭐⭐ | 5 分钟 | Docker: 一行命令 |
| OpenAI Key | ❌ 否 | ⭐ | 10 分钟 | 注册 + 复制 + 配置 |
| 阿里云 Key | ❌ 否 | ⭐⭐ | 20 分钟 | 注册 + 认证 + 复制 + 配置 |

\* PostgreSQL 可以用 Docker 替代，不需要本地安装

---

## ❌ 不需要做的事

```
❌ 安装 Git（已有 .git 文件夹）
❌ 手动创建数据库表（自动创建）
❌ 配置 NGINX（开发无需）
❌ 配置 SSL/HTTPS（开发无需）
❌ 配置用户认证（开发无需）
❌ 修改代码（可用但无需）
```

---

## 🎬 典型配置流程（按场景）

### 场景 1: 全新 Windows 电脑

```
总耗时: 1 小时

Step 1 (10 分钟): 安装 Python
  → 官网下载 installer
  → 勾选 "Add Python to PATH"
  → 安装

Step 2 (10 分钟): 安装 Node.js
  → 官网下载 installer
  → 默认安装

Step 3 (10 分钟): 安装 Docker
  → 官网下载 Docker Desktop
  → 默认安装

Step 4 (5 分钟): 验证安装
  → python --version
  → node --version
  → docker --version

Step 5 (10 分钟): 启动 PostgreSQL
  → docker run --name postgres_ai ...

Step 6 (5 分钟): 启动系统
  → .\启动.ps1

Step 7 (5 分钟): 验证系统
  → 访问 http://localhost:3000
  → 提交问题
  → 看到答案 ✅
```

---

### 场景 2: 已有 Python + Node.js

```
总耗时: 20 分钟

Step 1 (5 分钟): 安装 Docker（如果没装）
Step 2 (5 分钟): 启动 PostgreSQL
  → docker run --name postgres_ai ...
Step 3 (5 分钟): 启动系统
  → .\启动.ps1
Step 4 (5 分钟): 验证
  → 访问 http://localhost:3000 ✅
```

---

### 场景 3: 想要高质量答案

```
总耗时: 30 分钟

Step 1 (5 分钟): 完成基础配置（场景 1 或 2）
Step 2 (10 分钟): 获取 OpenAI API Key
  → https://platform.openai.com/api-keys
  → 注册 → 复制 Key
Step 3 (5 分钟): 更新 backend/.env
  → 设置 LLM_PROVIDER=openai
  → 设置 OPENAI_API_KEY=sk-xxx
Step 4 (5 分钟): 重启后端
  → Ctrl+C 停止
  → 重新运行 uvicorn 命令
Step 5 (5 分钟): 验证
  → 提交问题
  → 快速获得高质量答案 ✅
```

---

## 📞 配置问题速查

| 问题 | 症状 | 解决方案 |
|------|------|--------|
| Python 找不到 | `python: command not found` | 重装 + 勾选 "Add Python to PATH" |
| Node 找不到 | `node: command not found` | 重启 Shell，或重装 Node.js |
| PostgreSQL 连接失败 | `could not connect to server` | 运行 Docker 命令启动 |
| API Key 无效 | `Invalid API key` | 去官网重新生成 Key |
| 答案很慢 | 30-60 秒才有答案 | 正常（本地模型）/ 配置 OpenAI 快 10 倍 |
| 找不到 .env 文件 | 无法编辑配置 | 创建 `backend/.env` 文件 |

---

## ✨ 最终检查清单

启动前检查：

- [ ] Python 3.8+ 已装（`python --version`）
- [ ] Node.js 16+ 已装（`node --version`）
- [ ] Docker 已装（`docker --version`）
- [ ] PostgreSQL 运行中（`docker ps` 显示 postgres_ai）

启动：
- [ ] 运行 `.\启动.ps1`
- [ ] 等待 2-3 分钟
- [ ] 浏览器自动打开 http://localhost:3000

成功：
- [ ] 看到输入框
- [ ] 提交问题成功
- [ ] 获得答案

可选增强：
- [ ] 获取 OpenAI API Key（需要时）
- [ ] 更新 .env 配置
- [ ] 重启后端
- [ ] 验证答案质量提升

---

**一切就绪？运行：** `.\启动.ps1` ✨
