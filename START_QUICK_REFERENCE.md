# 🚀 启动快速参考 (Start Quick Reference)

**打印这个页面！** | 最后更新：2024-12-17

---

## 3 个启动命令 (Choose One)

### 1️⃣ 最简单（推荐）- 5 分钟

```powershell
cd "d:\桌面\AI"
.\启动.ps1
```

**发生了什么：**
- 自动检查 Python / Node.js / PostgreSQL
- 自动安装所有依赖
- 自动启动后端和前端
- 自动打开浏览器到 http://localhost:3000

**预期输出：**
```
✓ Backend running on http://localhost:8000
✓ Frontend running on http://localhost:3000
✓ Browser opened
```

---

### 2️⃣ 手动控制（开发者）- 10 分钟

**终端 1 - 数据库：**
```powershell
docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15
```

**终端 2 - 后端：**
```powershell
cd "d:\桌面\AI\backend"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**终端 3 - 前端：**
```powershell
cd "d:\桌面\AI\frontend"
npm install
npm run dev
```

**然后：** 访问 http://localhost:3000

---

### 3️⃣ Docker（生产环境）- 10 分钟

```powershell
cd "d:\桌面\AI"
docker-compose up --build
```

**预期输出（2 分钟后）：**
```
web      | INFO: Uvicorn running on http://0.0.0.0:8000
frontend | - ready started server on 0.0.0.0:3000
```

**然后：** 访问 http://localhost:3000

---

## ✅ 快速验证 (30 秒)

### 检查后端
```powershell
curl http://localhost:8000/health
```

预期：`{"status":"ok","message":"API is running"}`

或在浏览器访问：http://localhost:8000/docs

---

### 检查前端
浏览器访问：http://localhost:3000

应该看到：
- 📝 大输入框（输入问题）
- 🔘 蓝色按钮（提交）
- 📋 历史记录区域

---

## 🧪 5 分钟快速测试

### 测试 1: 提交问题（1 分钟）
```
输入：What is Python?
点击：提交问题
等待：10-30 秒
看到：答案显示在下方
```

### 测试 2: 评分（1 分钟）
```
点击：答案下方第 4 颗星
输入：Very helpful
点击：提交评分
看到：成功提示
```

### 测试 3: 查看历史（1 分钟）
```
向下滚动
看到：刚才的问题和答案
看到：时间戳和模型名
```

### 测试 4: 删除（1 分钟）
```
点击：任何历史记录的删除按钮
确认：删除
看到：记录消失
```

### 测试 5: 分页（1 分钟）
```
再提交 3-4 个问题
看到：分页按钮（如果 > 10 条）
点击：第 2 页
看到：下一页的记录
```

---

## ⚠️ 快速故障排除

| 问题 | 解决方案 |
|------|--------|
| **无法连接 localhost:8000** | 后端未启动。运行 `.\启动.ps1` |
| **npm 安装失败** | 清除缓存：`npm cache clean --force` |
| **PostgreSQL 连接失败** | 启动 Docker：`docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15` |
| **页面加载很慢** | 等待 10 秒。首次加载需要编译。 |
| **答案生成很慢** | 正常。本地模型需要 30-60 秒。换 OpenAI 会快 10 倍。 |
| **"Cannot GET /"** | 前端未启动。运行 `npm run dev` |
| **CORS 错误** | 更新 backend/.env 中的 CORS 设置 |

---

## 🔧 环境检查

```powershell
# 运行这个检查所有依赖
.\检查环境.ps1

# 或手动检查：
python --version      # 应该 >= 3.8
node --version        # 应该 >= 16
npm --version         # 应该 >= 8
docker --version      # 可选，用于 PostgreSQL
```

---

## 📁 文件位置

```
d:\桌面\AI\
├─ 后端代码: backend/app/*.py
├─ 前端代码: frontend/src/pages/*.tsx
├─ 启动脚本: .\启动.ps1
├─ 详细指南: MANUAL_STARTUP.md
├─ 测试指南: TESTING_GUIDE.md
├─ Docker 指南: DOCKER_GUIDE.md
└─ 项目总结: PROJECT_SUMMARY.md
```

---

## 🎯 成功标志

✅ 能访问 http://localhost:3000  
✅ 页面加载无错误  
✅ 能提交问题  
✅ 能获取答案  
✅ 能评分和删除  

**所有都 ✅？** 那你已经成功了！🎉

---

## 📞 需要帮助？

| 问题类型 | 查看文档 |
|---------|--------|
| 无法启动 | [MANUAL_STARTUP.md](MANUAL_STARTUP.md) |
| 功能不工作 | [TESTING_GUIDE.md](TESTING_GUIDE.md) |
| 想用 Docker | [DOCKER_GUIDE.md](DOCKER_GUIDE.md) |
| 想理解代码 | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| 完整检查表 | [PROJECT_COMPLETION_REPORT.md](PROJECT_COMPLETION_REPORT.md) |

---

## 🔑 API 密钥（可选）

### 使用本地模型（默认）
✅ 无需任何配置  
✅ 无需网络  
✅ 答案质量：中等  
✅ 速度：30-60 秒  

### 使用 OpenAI（可选）

1. 获取 Key：https://platform.openai.com/api-keys
2. 编辑 `backend/.env`：
   ```
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-your-key
   ```
3. 重启后端

**优势：** 答案质量高，速度快（5-10 秒）

### 使用 Alibaba Cloud（可选）

1. 获取 Key：https://dashscope.aliyun.com
2. 编辑 `backend/.env`：
   ```
   LLM_PROVIDER=alibaba
   ALIBABA_API_KEY=your-key
   ```
3. 重启后端

---

## ⏱️ 典型时间表

```
0:00 - 启动脚本
0:30 - 依赖安装完成
1:00 - 后端启动
1:30 - 前端启动
2:00 - 浏览器打开，首页加载
2:30 - 提交第一个问题
3:00 - 答案生成完成（本地模型）
3:30 - 完成测试
```

**总计：** 3-4 分钟（使用自动脚本）

---

## 💾 数据备份

所有数据自动保存在 PostgreSQL 数据库中。

**位置：** `postgres://localhost:5432/ai_qa`

**导出数据：**
```sql
-- 连接数据库后执行
SELECT * FROM questions;
```

**使用 Docker 时：**
```powershell
docker-compose exec postgres pg_dump -U postgres ai_qa > backup.sql
```

---

## 🔄 重启服务

### 重启后端
1. 按 `Ctrl+C` 停止
2. 重新运行启动命令

### 重启前端
1. 按 `Ctrl+C` 停止
2. 重新运行 `npm run dev`

### 重启数据库
```powershell
docker restart postgres
```

### 完全重置
```powershell
# 删除所有容器和数据
docker-compose down -v
# 重新启动
docker-compose up --build
```

---

## 📊 性能基准

| 操作 | 时间 | 使用 |
|------|------|------|
| 页面加载 | 2-3 秒 | 首次加载需要编译 |
| 问题提交 | 1 秒 | 网络和 DB 操作 |
| 答案生成（本地） | 30-60 秒 | CPU 密集操作 |
| 答案生成（OpenAI） | 5-10 秒 | API 调用 |
| 历史加载 | < 1 秒 | 快速查询 |
| 评分保存 | < 1 秒 | 数据库更新 |

---

## 🎓 学习路径

### 1️⃣ 新手 (15 分钟)
- 运行 `.\启动.ps1`
- 测试基本功能
- 阅读 [README.md](README.md)

### 2️⃣ 开发者 (1 小时)
- 阅读 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- 查看代码结构
- 运行手动启动步骤

### 3️⃣ 运维 (1 小时)
- 阅读 [DOCKER_GUIDE.md](DOCKER_GUIDE.md)
- 运行 Docker 版本
- 学习备份和恢复

### 4️⃣ 测试 (2 小时)
- 阅读 [TESTING_GUIDE.md](TESTING_GUIDE.md)
- 执行所有测试场景
- 记录性能指标

---

## ✨ 功能亮点

🎯 **直接问答** - 提问即答，无需上传文档  
🤖 **多个 LLM** - OpenAI / Alibaba / 本地模型  
⭐ **用户评分** - 5 星评价系统  
📝 **完整历史** - 所有问答自动保存  
🔒 **数据持久化** - PostgreSQL 数据库  
🚀 **生产就绪** - Docker / 云平台支持  

---

**准备好了？运行：** `.\启动.ps1` ✨

**需要详细指南？** 看 [MANUAL_STARTUP.md](MANUAL_STARTUP.md)

**遇到问题？** 查看 [TESTING_GUIDE.md](TESTING_GUIDE.md)

---

版本：1.0.0 | 更新：2024-12-17
