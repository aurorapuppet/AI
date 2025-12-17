# 前端 UI 说明

## 页面结构

### 首页 (pages/index.tsx)
主要交互页面，包含以下功能：
- **问题输入区**：用户输入问题的文本框
- **答案显示区**：展示 LLM 的回答结果
- **评分与反馈**：用户可以对答案评分（1-5星）并留下反馈
- **历史记录列表**：展示之前的问题与答案
- **分页功能**：支持上一页/下一页切换

## 组件结构

### QuestionForm.tsx
- 功能：问题输入表单
- Props:
  - `onSubmit(question)` - 提交问题的回调函数
  - `isLoading` - 是否处理中的状态
- 特性：
  - 自动禁用空白提交
  - Loading 状态显示处理中提示
  - Tailwind 样式美化

### AnswerDisplay.tsx
- 功能：答案展示与评分
- Props:
  - `question` - 问题文本
  - `answer` - 答案文本
  - `llmProvider` - 使用的 LLM 模型名称
  - `onRate(rating, feedback)` - 评分回调函数
- 特性：
  - 显示问题和答案
  - 5 星评分系统
  - 反馈文本框
  - 展开/收起评分表单

### HistoryList.tsx
- 功能：历史记录展示
- Props:
  - `questions` - 问题列表
  - `onSelectQuestion(question)` - 选中问题的回调
  - `onDeleteQuestion(id)` - 删除问题的回调
  - `isDeleting` - 删除中的状态
- 特性：
  - 列表展示问题摘要
  - 显示时间戳
  - 显示评分星级
  - 删除按钮

## API 调用 (lib/api.ts)

包含以下函数：

```typescript
// 提交问题，获取答案
askQuestion(question: string)
// 返回: { id, question_text, answer_text, llm_provider }

// 获取历史问题列表
getQuestions(skip?: number, limit?: number)
// 返回: Question[]

// 获取单个问题详情
getQuestion(id: number)
// 返回: Question

// 评分答案
rateAnswer(id: number, rating: number, feedback?: string)
// 返回: 评分结果

// 删除问题
deleteQuestion(id: number)
// 返回: 删除结果
```

## 状态管理

使用 React Hooks（useState, useEffect）管理：
- `currentAnswer` - 当前显示的答案
- `history` - 历史问题列表
- `isLoading` - 处理中状态
- `isDeleting` - 删除中状态
- `error` - 错误信息
- `skip` - 分页偏移量

## 样式

使用 Tailwind CSS：
- 渐变背景：蓝色到靛蓝
- 响应式设计：最大宽度 4xl（56rem）
- 卡片样式：白色背景，阴影效果
- 交互反馈：hover 效果、focus 状态

## 环境变量

在 `.env.local` 配置后端 URL：
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

默认值为 `http://localhost:8000`

## 启动前端

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:3000`

## 调试提示

1. 打开浏览器开发者工具（F12）查看网络请求
2. 检查 Console 标签页查看 JavaScript 错误
3. 确保后端服务运行在 `http://localhost:8000`
4. 检查 .env.local 中的 API URL 配置
