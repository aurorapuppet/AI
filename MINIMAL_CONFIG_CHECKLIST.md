# 📋 配置清单（最精简版）

> **你问的问题答案在这里。** 一页纸解决所有配置疑问。

---

## ✅ 必需配置（必须做）

### 1. Python 3.8+

**检查是否装了：**
```powershell
python --version
```

**如果没装：**
- 访问：https://www.python.org/downloads/
- 下载最新版
- ⚠️ **安装时勾选 "Add Python to PATH"**
- 重启 PowerShell，再检查一遍

---

### 2. Node.js 16+

**检查是否装了：**
```powershell
node --version
npm --version
```

**如果没装：**
- 访问：https://nodejs.org/
- 下载 LTS 版本（左边大按钮）
- 默认安装即可
- 重启 PowerShell，再检查一遍

---

### 3. PostgreSQL 数据库

**方案 A：Docker（推荐）- 最简单**

```powershell
# 需要先装 Docker Desktop
# https://www.docker.com/products/docker-desktop/

# 然后一行命令启动数据库：
docker run --name postgres_ai -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# 验证：
docker ps
```

**方案 B：本地安装（不推荐，较复杂）**
- 访问：https://www.postgresql.org/download/windows/
- 下载 PostgreSQL 15
- 安装时记住 postgres 用户密码
- 完成

---

## 🟢 可选配置（增强答案质量）

### 4. OpenAI API（推荐）

**为什么要配：** 答案快 10 倍（5-10 秒 vs 30-60 秒）

**获取步骤：**
1. 访问：https://platform.openai.com/signup
2. 注册账号（邮箱/Google/Microsoft）
3. 访问：https://platform.openai.com/api-keys
4. 点击 "Create new secret key"
5. 复制生成的 Key（格式：`sk-xxxxxxx`）

**配置步骤：**
1. 编辑文件：`backend/.env`
2. 找到这两行：
   ```
   LLM_PROVIDER=local
   # OPENAI_API_KEY=sk-xxxxx
   ```
3. 改成：
   ```
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-你复制的key
   ```
4. 保存文件
5. 重启后端（Ctrl+C 停止，重新运行启动命令）

**成本：** 新账号 $5 免费额度

---

### 5. 阿里云千问 API（可选）

**为什么要配：** 中文优化好，价格便宜

**获取步骤：**
1. 访问：https://www.aliyun.com/
2. 点击 "免费注册"
3. 用手机号注册 + 实名认证
4. 访问：https://dashscope.aliyun.com/
5. 点击 "开通服务"
6. 左侧菜单 "API-KEY" → "创建新的API-KEY"
7. 复制生成的 Key

**配置步骤：**
1. 编辑文件：`backend/.env`
2. 改成：
   ```
   LLM_PROVIDER=alibaba
   DASHSCOPE_API_KEY=sk-你复制的key
   ```
3. 保存文件
4. 重启后端

**成本：** 有免费额度，按量计费

---

## 📊 对比表

| 功能 | 必需? | 难度 | 时间 | 下载/获取 |
|------|-------|------|------|----------|
| **Python** | ✅ | ⭐ | 5 分钟 | https://python.org |
| **Node.js** | ✅ | ⭐ | 5 分钟 | https://nodejs.org |
| **PostgreSQL** | ✅ | ⭐⭐ | 5 分钟 (Docker) | Docker 镜像 |
| **OpenAI API** | ❌ | ⭐ | 10 分钟 | https://openai.com |
| **阿里云 API** | ❌ | ⭐⭐ | 20 分钟 | https://dashscope.aliyun.com |

---

## 🎯 最小启动方案（15 分钟）

**假设已有 Python 3.8+ 和 Node.js 16+**

```powershell
# 1. 启动 PostgreSQL（Docker）
docker run --name postgres_ai -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# 2. 启动系统
cd "d:\桌面\AI"
.\启动.ps1

# 3. 访问
http://localhost:3000

# 完成！系统可用，答案质量中等
```

---

## 🚀 完整启动方案（30 分钟，答案优秀）

```powershell
# 1-2. 确保 Python 和 Node.js 已装

# 3. 启动 PostgreSQL
docker run --name postgres_ai -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15

# 4. 获取 OpenAI API Key
# → 访问 https://platform.openai.com/api-keys
# → 复制你的 Key

# 5. 编辑 backend/.env
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-你的key

# 6. 启动系统
cd "d:\桌面\AI"
.\启动.ps1

# 7. 访问并测试
http://localhost:3000

# 完成！系统可用，答案快速优质
```

---

## ❓ 常见问题

**Q: 一定要装 PostgreSQL 吗？**
A: 是的，但用 Docker 比本地装简单 100 倍。

**Q: 没有 API Key 能用吗？**
A: 能。用本地 GPT-2 模型，免费但较慢（30-60 秒）。

**Q: OpenAI 和阿里云哪个好？**
A: OpenAI 更强，阿里云中文更好。都配置的话可以随时切换。

**Q: API 会花钱吗？**
A: 新注册 OpenAI 有 $5 免费额度。用完再付费，每 1000 词约 $0.0005。

**Q: 配置好了怎么验证？**
A: 访问 http://localhost:3000，提交问题，看到答案就成功了。

---

## 📑 详细指南

| 需要 | 查看文件 |
|------|--------|
| 详细的 Python 安装说明 | [SETUP_CONFIGURATION_GUIDE.md](SETUP_CONFIGURATION_GUIDE.md) |
| 详细的 API Key 获取步骤 | [SETUP_CONFIGURATION_GUIDE.md](SETUP_CONFIGURATION_GUIDE.md) |
| 详细的配置修改 | [SETUP_CONFIGURATION_GUIDE.md](SETUP_CONFIGURATION_GUIDE.md) |
| 快速启动命令 | [START_QUICK_REFERENCE.md](START_QUICK_REFERENCE.md) |
| 完整项目状态 | [PROJECT_COMPLETION_REPORT.md](PROJECT_COMPLETION_REPORT.md) |

---

## ✨ 总结

**最少需要：** Python + Node.js + PostgreSQL（Docker）= 15 分钟

**建议配置：** + OpenAI API = 25 分钟 → 快速优质答案

**完整配置：** + 阿里云 API = 35 分钟 → 灵活切换

---

**准备好了？** 运行 `.\启动.ps1` 🚀
