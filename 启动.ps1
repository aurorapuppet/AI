#!/usr/bin/env pwsh

# AI 智能问答平台 - PowerShell 启动脚本

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host " AI 智能问答平台 - 启动助手" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# 检查 Python
Write-Host "[1/6] 检查 Python 环境..." -ForegroundColor Yellow
try {
    python --version | Out-Null
    Write-Host "✅ Python 已安装" -ForegroundColor Green
} catch {
    Write-Host "❌ 错误: 未找到 Python" -ForegroundColor Red
    exit 1
}

# 检查 Node.js
Write-Host "[2/6] 检查 Node.js 环境..." -ForegroundColor Yellow
try {
    node --version | Out-Null
    Write-Host "✅ Node.js 已安装" -ForegroundColor Green
} catch {
    Write-Host "❌ 错误: 未找到 Node.js" -ForegroundColor Red
    exit 1
}

# 检查 PostgreSQL
Write-Host "[3/6] 检查 PostgreSQL..." -ForegroundColor Yellow
$postgresCheck = & {
    try {
        psql --version 2>$null
        return $true
    } catch {
        return $false
    }
}

if (-not $postgresCheck) {
    Write-Host "⚠️  PostgreSQL 未运行" -ForegroundColor Yellow
    $start_postgres = Read-Host "是否启动 PostgreSQL Docker 容器? (Y/N)"
    if ($start_postgres -eq "Y" -or $start_postgres -eq "y") {
        Write-Host "正在启动 PostgreSQL..." -ForegroundColor Cyan
        docker run --name postgres-ai -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:15
        Start-Sleep -Seconds 5
        docker exec postgres-ai psql -U postgres -c "CREATE DATABASE ai_qa;" 2>$null
        Write-Host "✅ PostgreSQL 已启动" -ForegroundColor Green
    }
} else {
    Write-Host "✅ PostgreSQL 已运行" -ForegroundColor Green
}

# 安装后端依赖
Write-Host "[4/6] 安装后端依赖..." -ForegroundColor Yellow
Push-Location "d:\桌面\AI\backend"
if (-not (Test-Path "venv")) {
    python -m venv venv
}
& ".\venv\Scripts\Activate.ps1"
pip install -r requirements.txt -q
Write-Host "✅ 后端依赖已安装" -ForegroundColor Green
Pop-Location

# 初始化数据库
Write-Host "[5/6] 初始化数据库..." -ForegroundColor Yellow
Push-Location "d:\桌面\AI\backend"
& ".\venv\Scripts\Activate.ps1"
python -c "from app.db import create_tables; create_tables()" 2>$null
Write-Host "✅ 数据库已初始化" -ForegroundColor Green
Pop-Location

# 启动后端
Write-Host "[6/6] 启动后端和前端..." -ForegroundColor Yellow

# 启动后端（新窗口）
$backendProcess = Start-Process powershell -PassThru -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd 'd:\桌面\AI\backend'; .\venv\Scripts\Activate.ps1; Write-Host 'Backend starting...' -ForegroundColor Green; uvicorn app.main:app --reload --port 8000"
)

Write-Host "✅ 后端进程启动中 (PID: $($backendProcess.Id))" -ForegroundColor Green

Start-Sleep -Seconds 5

# 安装前端依赖
Write-Host "安装前端依赖..." -ForegroundColor Cyan
Push-Location "d:\桌面\AI\frontend"
npm install -q 2>$null
Write-Host "✅ 前端依赖已安装" -ForegroundColor Green
Pop-Location

# 启动前端（新窗口）
$frontendProcess = Start-Process powershell -PassThru -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd 'd:\桌面\AI\frontend'; Write-Host 'Frontend starting...' -ForegroundColor Green; npm run dev"
)

Write-Host "✅ 前端进程启动中 (PID: $($frontendProcess.Id))" -ForegroundColor Green

# 打开浏览器
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host " ✅ 启动完成！" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📍 访问地址:" -ForegroundColor Yellow
Write-Host "   前端应用:  http://localhost:3000" -ForegroundColor Cyan
Write-Host "   API 文档:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "   ReDoc:    http://localhost:8000/redoc" -ForegroundColor Cyan

Write-Host "`n⏳ 等待服务启动（约 10-15 秒）..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "📂 打开浏览器..." -ForegroundColor Green
Start-Process "http://localhost:3000"

Write-Host "`n💡 提示:" -ForegroundColor Yellow
Write-Host "   - 按 Ctrl+C 停止任何服务" -ForegroundColor Gray
Write-Host "   - 查看 TESTING_GUIDE.md 了解详细测试步骤" -ForegroundColor Gray
Write-Host "   - 前后端日志将显示在各自的窗口中" -ForegroundColor Gray

Write-Host "`n按任意键继续..." -ForegroundColor Gray
$null = Read-Host
