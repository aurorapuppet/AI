# 🧪 实际测试与验证指南

## 前置条件检查

### 1. 检查 PostgreSQL 数据库

**Windows PowerShell:**
```powershell
# 查看是否有 PostgreSQL 运行
Get-Process postgres -ErrorAction SilentlyContinue
```

**如果没有运行，需要安装或启动 PostgreSQL：**

#### 选项 A: 使用 Docker (推荐)
```powershell
# 启动 PostgreSQL Docker 容器
docker run --name postgres-ai -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:15

# 创建数据库
docker exec postgres-ai psql -U postgres -c "CREATE DATABASE ai_qa;"
```

#### 选项 B: 本地安装
- 下载 PostgreSQL: https://www.postgresql.org/download/windows/
- 安装时记住密码（默认用户 postgres）
- 创建数据库 `ai_qa`

### 2. 验证数据库连接

```powershell
# 安装 psql 客户端（或使用 DBeaver）
psql -h localhost -U postgres -d ai_qa

# 在 psql 中验证连接
\dt  # 列出所有表（首次应为空）
\q   # 退出
```

---

## 后端启动步骤

### Step 1: 进入后端目录
```powershell
cd "d:\桌面\AI\backend"
```

### Step 2: 创建虚拟环境
```powershell
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 如果出现权限错误，运行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: 安装依赖
```powershell
pip install -r requirements.txt
```

### Step 4: 初始化数据库
```powershell
# 创建数据库表
python -c "from app.db import create_tables; create_tables()"

# 验证表是否创建成功
psql -h localhost -U postgres -d ai_qa -c "\dt"
```

### Step 5: 启动后端服务
```powershell
# 开发模式启动（支持热重载）
uvicorn app.main:app --reload --port 8000

# 或者指定应用目录
uvicorn app.main:app --reload --app-dir app --port 8000
```

**成功标志：**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Step 6: 验证后端 API
在浏览器打开以下 URL：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 前端启动步骤（新终端窗口）

### Step 1: 进入前端目录
```powershell
cd "d:\桌面\AI\frontend"
```

### Step 2: 安装依赖
```powershell
npm install
```

### Step 3: 启动前端开发服务
```powershell
npm run dev
```

**成功标志：**
```
> ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

### Step 4: 打开浏览器
访问 http://localhost:3000

---

## 完整功能测试流程

### 🧪 测试 1: 后端 API 健康检查

**Swagger 文档位置：** http://localhost:8000/docs

**测试步骤：**
1. 点击 "GET /health"
2. 点击 "Try it out"
3. 点击 "Execute"
4. 应该看到状态 200 和响应 `{"status":"ok"}`

### 🧪 测试 2: 提交问题并获取答案

**在 Swagger 中：**
1. 找到 "POST /ask" 端点
2. 点击 "Try it out"
3. 在请求体中输入：
```json
{
  "question": "什么是机器学习？"
}
```
4. 点击 "Execute"
5. 应该收到包含以下内容的响应：
```json
{
  "id": 1,
  "question_text": "什么是机器学习？",
  "answer_text": "机器学习是...",
  "llm_provider": "local",
  "rating": null,
  "feedback": null,
  "created_at": "2024-12-17T...",
  "updated_at": "2024-12-17T..."
}
```

### 🧪 测试 3: 获取历史问答记录

**在 Swagger 中：**
1. 找到 "GET /questions" 端点
2. 点击 "Try it out"
3. 参数留空（使用默认 skip=0, limit=20）
4. 点击 "Execute"
5. 应该返回问答列表（包含之前添加的问题）

### 🧪 测试 4: 获取单个问答

**在 Swagger 中：**
1. 找到 "GET /questions/{id}" 端点
2. 输入 id: 1
3. 点击 "Execute"
4. 应该返回该问题的完整信息

### 🧪 测试 5: 评分答案

**在 Swagger 中：**
1. 找到 "POST /questions/{id}/rate" 端点
2. 输入 id: 1
3. 在请求体中输入：
```json
{
  "question_id": 1,
  "rating": 5,
  "feedback": "非常有帮助的答案！"
}
```
4. 点击 "Execute"
5. 应该返回更新成功的响应

### 🧪 测试 6: 删除问答

**在 Swagger 中：**
1. 找到 "DELETE /questions/{id}" 端点
2. 输入 id: 1
3. 点击 "Execute"
4. 应该返回删除成功

---

## 前端用户交互测试

### 🧪 前端测试 1: 页面加载

**步骤：**
1. 打开 http://localhost:3000
2. 检查以下元素是否存在：
   - ✅ 标题 "AI 智能问答平台"
   - ✅ 问题输入框
   - ✅ "获取答案" 按钮
   - ✅ 历史记录列表（可能为空）

### 🧪 前端测试 2: 输入问题

**步骤：**
1. 在问题输入框输入：`Python 中 list 和 tuple 有什么区别？`
2. 检查：
   - ✅ 提交按钮启用（蓝色）
   - ✅ 输入框接受文字

### 🧪 前端测试 3: 提交问题获取答案

**步骤：**
1. 点击 "获取答案" 按钮
2. 等待 LLM 生成答案（可能需要 5-30 秒）
3. 检查：
   - ✅ Loading 状态显示（⚙️ 处理中...）
   - ✅ 答案区域出现
   - ✅ 显示问题和答案
   - ✅ 显示使用的 LLM 模型名称

### 🧪 前端测试 4: 评分答案

**步骤：**
1. 在答案下方点击 "评分此答案"
2. 检查评分表单：
   - ✅ 5 个星形符号出现
   - ✅ 可以点击选择星级
3. 点击第 5 个星（5 星）
4. 在反馈框输入：`回答很准确`
5. 点击 "提交评分"
6. 检查：
   - ✅ 显示成功提示
   - ✅ 表单收起

### 🧪 前端测试 5: 查看历史记录

**步骤：**
1. 向下滚动到历史记录部分
2. 检查：
   - ✅ 新添加的问题出现在列表中
   - ✅ 显示问题摘要
   - ✅ 显示时间戳
   - ✅ 显示 5 星评分

### 🧪 前端测试 6: 点击历史项查看详情

**步骤：**
1. 点击历史列表中的一条记录
2. 检查：
   - ✅ 页面滚动到顶部
   - ✅ 答案区域显示该问答
   - ✅ 信息与列表中一致

### 🧪 前端测试 7: 删除问答

**步骤：**
1. 在历史列表中找到一条记录
2. 点击 "删除" 按钮
3. 确认删除对话框
4. 检查：
   - ✅ 记录从列表移除
   - ✅ 数据库中的记录被删除

### 🧪 前端测试 8: 分页功能

**步骤：**
1. 提交多个问题（超过 10 个）
2. 检查：
   - ✅ 第一页显示 10 条记录
   - ✅ "下一页" 按钮启用
3. 点击 "下一页"
4. 检查：
   - ✅ 显示下一页的记录
   - ✅ "上一页" 按钮启用

---

## 网络请求验证（浏览器开发者工具）

### 打开浏览器控制台

**步骤：**
1. 按 F12 打开开发者工具
2. 切换到 "Network" 标签页
3. 在网页中执行操作

### 验证请求 1: POST /ask

**操作：** 提交问题
**检查：**
- ✅ 请求方法：POST
- ✅ URL：http://localhost:8000/ask
- ✅ 请求体包含 `{"question": "..."}`
- ✅ 响应状态：200
- ✅ 响应包含 `id, question_text, answer_text, llm_provider`

### 验证请求 2: GET /questions

**操作：** 页面加载或刷新
**检查：**
- ✅ 请求方法：GET
- ✅ URL：http://localhost:8000/questions?skip=0&limit=10
- ✅ 响应状态：200
- ✅ 响应是数组格式

### 验证请求 3: POST /questions/{id}/rate

**操作：** 提交评分
**检查：**
- ✅ 请求方法：POST
- ✅ 请求体包含 `{question_id, rating, feedback}`
- ✅ 响应状态：200

### 验证请求 4: DELETE /questions/{id}

**操作：** 删除问答
**检查：**
- ✅ 请求方法：DELETE
- ✅ 响应状态：200

---

## 错误处理测试

### ❌ 测试 1: 后端离线

**操作：** 停止后端服务，在前端提交问题

**预期结果：**
- ✅ 前端显示错误提示：`"获取答案失败，请检查后端服务是否运行"`
- ✅ 页面不崩溃
- ✅ 可以重新尝试

### ❌ 测试 2: 数据库离线

**操作：** 停止 PostgreSQL，提交问题

**预期结果：**
- ✅ 后端返回 500 错误
- ✅ 前端显示错误信息
- ✅ 控制台显示数据库连接错误

### ❌ 测试 3: 网络延迟

**操作：** 打开浏览器开发者工具，限制网络速度，提交问题

**预期结果：**
- ✅ Loading 状态正常显示
- ✅ 最终能够成功加载答案
- ✅ 没有超时错误

---

## 性能测试

### 📊 测试 1: 页面加载时间

**工具：** Chrome DevTools - Performance 标签

**目标：** < 3 秒

```powershell
# 在浏览器中：
# 1. 按 F12
# 2. 切换到 "Performance" 标签
# 3. 点击刷新按钮
# 4. 等待加载完成
# 5. 查看 "Largest Contentful Paint (LCP)"
```

### 📊 测试 2: 获取答案响应时间

**目标：** < 30 秒（取决于 LLM 速度）

```powershell
# 在浏览器 Network 标签中：
# 1. 清除网络记录
# 2. 提交问题
# 3. 查看 POST /ask 请求的 Time 列
# 4. 记录完成时间
```

### 📊 测试 3: 历史列表加载

**目标：** < 2 秒

```powershell
# 在浏览器 Network 标签中：
# 1. 页面加载时查看 GET /questions 请求
# 2. 记录响应时间
```

---

## LLM API 密钥配置（可选）

### 使用 OpenAI

1. **获取 API Key**
   - 访问 https://platform.openai.com/api-keys
   - 创建新的 API Key
   - 复制密钥

2. **配置 .env**
   ```bash
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-your-key-here
   ```

3. **重启后端**
   ```powershell
   # 停止服务（Ctrl+C）
   # 重新启动
   uvicorn app.main:app --reload --port 8000
   ```

### 使用 Alibaba Cloud

1. **获取 API Key**
   - 访问 https://dashscope.aliyun.com
   - 获取 API Key

2. **配置 .env**
   ```bash
   LLM_PROVIDER=alibaba
   DASHSCOPE_API_KEY=sk-your-key-here
   ```

3. **重启后端**

---

## 测试清单

| 测试项 | 状态 | 备注 |
|--------|------|------|
| PostgreSQL 连接 | ⬜ | |
| 后端启动 | ⬜ | |
| 前端启动 | ⬜ | |
| API 健康检查 | ⬜ | |
| 提交问题 | ⬜ | |
| 获取答案 | ⬜ | |
| 查看历史 | ⬜ | |
| 评分答案 | ⬜ | |
| 删除记录 | ⬜ | |
| 前端页面加载 | ⬜ | |
| 前端问题提交 | ⬜ | |
| 前端评分功能 | ⬜ | |
| 前端删除功能 | ⬜ | |
| 错误处理 | ⬜ | |
| 性能指标 | ⬜ | |

---

## 常见问题排查

### ❓ 问题 1: 后端无法启动

**错误：** `ModuleNotFoundError: No module named 'fastapi'`

**解决：**
```powershell
pip install -r requirements.txt
```

### ❓ 问题 2: 数据库连接失败

**错误：** `could not connect to server: Connection refused`

**解决：**
```powershell
# 确保 PostgreSQL 运行中
docker ps  # 或检查 Windows 服务中的 PostgreSQL
```

### ❓ 问题 3: 前端无法访问后端

**错误：** `Failed to fetch` 或 CORS 错误

**解决：**
1. 检查后端是否运行在 8000 端口
2. 检查前端 .env.local 中的 NEXT_PUBLIC_API_URL
3. 检查防火墙设置

### ❓ 问题 4: LLM 调用失败

**错误：** `Invalid API Key` 或 `Rate limit exceeded`

**解决：**
1. 检查 API Key 配置
2. 使用 local 模型进行测试（不需要 API Key）
3. 检查网络连接

---

## 下一步

✅ **所有测试通过后：**
1. 使用真实 LLM API Key 进行完整测试
2. 进行压力测试（并发请求）
3. 准备 Docker 部署
4. 添加自动化测试套件
