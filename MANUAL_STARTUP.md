# 🚀 完整启动与测试指南 (Windows PowerShell)

## 快速启动（自动化）

### 方法 1: 运行 PowerShell 脚本

```powershell
# 进入项目目录
cd "d:\桌面\AI"

# 运行启动脚本
.\启动.ps1
```

这个脚本将自动：
1. 检查环境（Python、Node.js、PostgreSQL）
2. 启动 PostgreSQL（如果需要）
3. 安装依赖
4. 初始化数据库
5. 启动后端和前端
6. 打开浏览器

---

## 手动启动（详细步骤）

### 📌 前置条件

#### 1. 安装必要软件

**Python 3.8+**
```powershell
python --version
# 如果没有，下载: https://www.python.org/downloads/
```

**Node.js 16+**
```powershell
node --version
npm --version
# 如果没有，下载: https://nodejs.org/
```

**PostgreSQL 15 (或 Docker)**
```powershell
# 方法 A: 使用 Docker (推荐)
docker --version
# 如果没有，下载: https://www.docker.com/

# 方法 B: 本地安装
psql --version
# 如果没有，下载: https://www.postgresql.org/download/windows/
```

---

### 📌 启动 PostgreSQL

#### 方法 A: Docker (推荐)

**创建并启动容器：**
```powershell
# 启动 PostgreSQL 容器
docker run --name postgres-ai -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:15

# 创建数据库
docker exec postgres-ai psql -U postgres -c "CREATE DATABASE ai_qa;"

# 验证
docker ps
```

**停止容器（测试完后）：**
```powershell
docker stop postgres-ai
docker rm postgres-ai
```

#### 方法 B: 本地 PostgreSQL

**验证运行：**
```powershell
# 连接到数据库
psql -h localhost -U postgres

# 创建数据库（在 psql 中）
CREATE DATABASE ai_qa;
\q  # 退出
```

---

### 📌 启动后端服务

#### Step 1: 打开第一个 PowerShell 窗口

```powershell
# 进入后端目录
cd "d:\桌面\AI\backend"

# 查看当前目录
Get-ChildItem
# 应该看到: app/, requirements.txt, Dockerfile 等
```

#### Step 2: 创建虚拟环境（首次）

```powershell
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 如果出现错误，运行这个（一次性）：
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Step 3: 安装依赖

```powershell
# 确保已激活虚拟环境（提示符显示 (venv)）
pip install -r requirements.txt

# 验证安装
pip list | findstr fastapi
# 应该显示 fastapi 版本
```

#### Step 4: 初始化数据库

```powershell
# 创建数据库表
python -c "from app.db import create_tables; create_tables()"

# 验证表是否创建
psql -h localhost -U postgres -d ai_qa -c "\dt"
# 应该显示 "questions" 表
```

#### Step 5: 启动后端服务

```powershell
# 开发模式（支持热重载）
uvicorn app.main:app --reload --port 8000

# 成功标志：
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

**验证后端：**
- 浏览器打开: http://localhost:8000/health
- 应显示: `{"status":"ok"}`

---

### 📌 启动前端服务

#### Step 1: 打开第二个 PowerShell 窗口（不关闭第一个）

```powershell
# 进入前端目录
cd "d:\桌面\AI\frontend"

# 验证目录
Get-ChildItem
# 应该看到: pages/, components/, lib/, package.json 等
```

#### Step 2: 安装依赖

```powershell
npm install

# 首次安装可能需要 2-3 分钟
# 会创建 node_modules 文件夹
```

#### Step 3: 启动前端服务

```powershell
npm run dev

# 成功标志：
# > ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

#### Step 4: 打开浏览器

```powershell
# 在第三个窗口执行
start http://localhost:3000
```

---

## 🧪 完整功能测试

### 测试 1: 页面加载

1. 浏览器打开: http://localhost:3000
2. 检查以下元素：
   - ✅ 标题 "AI 智能问答平台"
   - ✅ 问题输入框
   - ✅ "获取答案" 按钮
   - ✅ 历史记录区域

**失败排查：**
- 如果看不到内容，检查浏览器控制台（F12）
- 查看 Network 标签，检查是否有 HTTP 错误

### 测试 2: 提交问题

1. 在输入框输入问题：
   ```
   Python 中 lambda 函数有什么用途？
   ```

2. 点击 "获取答案" 按钮

3. 等待答案生成（可能需要 5-30 秒，取决于 LLM）

4. 检查结果：
   - ✅ 显示答案文本
   - ✅ 显示 LLM 模型名称
   - ✅ 显示问题和答案对

**失败排查：**
- 如果显示错误: `"获取答案失败，请检查后端服务是否运行"`
  - 确保后端服务正常运行（第一个窗口）
  - 检查后端日志是否有错误
  - 尝试重新加载页面

### 测试 3: 评分答案

1. 在答案下方点击 "评分此答案"
2. 点击第 5 个星（5 星评分）
3. 在反馈框输入：`很有帮助`
4. 点击 "提交评分"
5. 应显示成功提示

### 测试 4: 查看历史

1. 向下滚动找到历史记录部分
2. 应显示刚才提交的问题
3. 点击历史项查看详情

### 测试 5: 删除记录

1. 在历史列表中找到一条记录
2. 点击 "删除" 按钮
3. 确认删除
4. 记录应从列表移除

### 测试 6: 分页

1. 提交多个问题（至少 15 个）
2. 查看分页按钮是否出现
3. 点击 "下一页"，应显示下一批记录

---

## 🔍 使用 API 文档进行测试（可选）

### 访问 Swagger 文档

```
http://localhost:8000/docs
```

### 在 Swagger 中测试 API

#### 测试端点 1: POST /ask

1. 找到 "POST /ask" 端点
2. 点击 "Try it out"
3. 在请求体中输入：
   ```json
   {
     "question": "什么是 REST API？"
   }
   ```
4. 点击 "Execute"
5. 应该收到包含 answer_text 的响应

#### 测试端点 2: GET /questions

1. 找到 "GET /questions" 端点
2. 点击 "Try it out"
3. 不修改参数，直接点击 "Execute"
4. 应该返回问答列表

#### 测试端点 3: POST /questions/{id}/rate

1. 找到 "POST /questions/{id}/rate" 端点
2. 输入 id (例如 1)
3. 在请求体中输入：
   ```json
   {
     "question_id": 1,
     "rating": 5,
     "feedback": "非常好"
   }
   ```
4. 点击 "Execute"
5. 应该返回更新成功

---

## 📊 检查网络请求（浏览器开发者工具）

### 打开开发者工具

```
按 F12 或右键点击 → 检查
```

### 查看 Network 标签

1. 切换到 "Network" 标签
2. 在网页中执行操作（提交问题、评分等）
3. 应该看到以下请求：

**POST /ask**
- 状态: 200
- 请求体: `{"question": "..."}`
- 响应: 包含 answer_text

**GET /questions**
- 状态: 200
- 查询参数: skip=0&limit=10
- 响应: 数组格式

**POST /questions/{id}/rate**
- 状态: 200
- 响应: 成功信息

---

## 🛑 停止服务

### 停止后端
在后端窗口：
```powershell
Ctrl + C
```

### 停止前端
在前端窗口：
```powershell
Ctrl + C
```

### 停止 PostgreSQL (Docker)
```powershell
docker stop postgres-ai
```

---

## ⚠️ 常见问题排查

### 问题 1: "端口 3000 已被占用"

```powershell
# 查找占用端口的进程
netstat -ano | findstr :3000

# 杀死进程（假设 PID 为 1234）
taskkill /PID 1234 /F
```

### 问题 2: "无法连接到数据库"

```powershell
# 确认 PostgreSQL 运行
docker ps  # 或检查 Windows 服务

# 测试连接
psql -h localhost -U postgres -d ai_qa -c "SELECT 1"
```

### 问题 3: "模块未找到"

```powershell
# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

### 问题 4: "LLM 回复为空或超时"

**原因可能：**
- 网络连接慢
- LLM 服务超时
- API Key 无效

**解决：**
1. 检查网络连接
2. 等待更长的时间
3. 配置有效的 API Key（如使用 OpenAI）

---

## 📈 使用真实 LLM API (可选)

### 配置 OpenAI

1. 获取 API Key: https://platform.openai.com/api-keys
2. 编辑 `backend/.env`:
   ```
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-your-key
   ```
3. 重启后端

### 配置 Alibaba Cloud

1. 获取 API Key: https://dashscope.aliyun.com
2. 编辑 `backend/.env`:
   ```
   LLM_PROVIDER=alibaba
   DASHSCOPE_API_KEY=sk-your-key
   ```
3. 重启后端

---

## 📝 测试记录模板

```markdown
# 测试记录 - 2024-12-17

## 环境
- Python: 3.10.0
- Node.js: v18.0.0
- PostgreSQL: 15
- 后端地址: http://localhost:8000
- 前端地址: http://localhost:3000

## 功能测试结果
- [ ] 页面加载 - 通过/失败
- [ ] 提交问题 - 通过/失败
- [ ] 获取答案 - 通过/失败
- [ ] 评分答案 - 通过/失败
- [ ] 查看历史 - 通过/失败
- [ ] 删除记录 - 通过/失败
- [ ] 分页功能 - 通过/失败

## 性能指标
- 页面加载时间: __ 秒
- 获取答案响应时间: __ 秒
- 历史加载时间: __ 秒

## 发现的问题
1. ...
2. ...

## 备注
...
```

---

## ✅ 下一步

测试完成后：
1. 使用真实 LLM API 进行完整测试
2. 进行压力测试（并发请求）
3. 准备 Docker 部署
4. 添加自动化测试套件

---

**如有问题，请参考:**
- TESTING_CHECKLIST.md - 详细检查清单
- FRONTEND_README.md - 前端组件说明
- PROJECT_SUMMARY.md - 技术细节
