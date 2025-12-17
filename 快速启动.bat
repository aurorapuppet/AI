@echo off
REM AI 智能问答平台 - 快速启动脚本（Windows PowerShell）

echo.
echo ========================================
echo  AI 智能问答平台 - 启动助手
echo ========================================
echo.

REM 检查 Python
echo [1/5] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)
echo ✅ Python 已安装

REM 检查 Node.js
echo [2/5] 检查 Node.js 环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Node.js，请先安装 Node.js
    pause
    exit /b 1
)
echo ✅ Node.js 已安装

REM 检查 PostgreSQL
echo [3/5] 检查 PostgreSQL...
where psql >nul 2>&1
if errorlevel 1 (
    echo ⚠️  警告: 未找到 PostgreSQL
    echo 请使用以下命令启动 PostgreSQL Docker 容器:
    echo docker run --name postgres-ai -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:15
    echo.
    set /p continue="是否继续? (Y/N): "
    if /i not "%continue%"=="Y" exit /b 1
) else (
    echo ✅ PostgreSQL 已安装
)

REM 打开新终端启动后端
echo [4/5] 启动后端服务...
echo 正在打开新的 PowerShell 窗口启动后端...
start powershell -NoExit -Command "cd 'd:\桌面\AI\backend'; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --port 8000"

REM 等待后端启动
timeout /t 5 /nobreak

REM 打开新终端启动前端
echo [5/5] 启动前端服务...
echo 正在打开新的 PowerShell 窗口启动前端...
start powershell -NoExit -Command "cd 'd:\桌面\AI\frontend'; npm run dev"

REM 打开浏览器
echo.
echo ========================================
echo ✅ 启动完成！
echo ========================================
echo.
echo 请访问以下地址:
echo   前端:     http://localhost:3000
echo   后端 API: http://localhost:8000/docs
echo.
echo 启动后端可能需要 5-10 秒。
echo.
timeout /t 3
start http://localhost:3000

pause
