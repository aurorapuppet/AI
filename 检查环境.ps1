#!/usr/bin/env pwsh

# AI 智能问答平台 - 环境检查脚本

Write-Host "`n" -ForegroundColor Cyan
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  AI 智能问答平台 - 环境检查             ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host "`n"

$checks = @(
    @{Name = "Python"; Command = "python --version"; Required = $true},
    @{Name = "Node.js"; Command = "node --version"; Required = $true},
    @{Name = "npm"; Command = "npm --version"; Required = $true},
    @{Name = "Git"; Command = "git --version"; Required = $false},
    @{Name = "Docker"; Command = "docker --version"; Required = $false},
    @{Name = "PostgreSQL"; Command = "psql --version"; Required = $false}
)

$passed = 0
$failed = 0
$warnings = 0

foreach ($check in $checks) {
    Write-Host "[检查] $($check.Name)..." -ForegroundColor Yellow -NoNewline
    
    try {
        $output = & ($check.Command.Split()[0]) ($check.Command.Split() | Select-Object -Skip 1) 2>&1 | Out-String
        Write-Host " ✅" -ForegroundColor Green
        Write-Host "       $output".Trim() -ForegroundColor Gray
        $passed++
    } catch {
        if ($check.Required) {
            Write-Host " ❌" -ForegroundColor Red
            Write-Host "       ⚠️ 必需组件缺失！" -ForegroundColor Red
            $failed++
        } else {
            Write-Host " ⚠️ (可选)" -ForegroundColor Yellow
            Write-Host "       此组件为可选，系统可正常运行" -ForegroundColor Gray
            $warnings++
        }
    }
    Write-Host ""
}

# 检查目录结构
Write-Host "[检查] 项目目录结构..." -ForegroundColor Yellow -NoNewline
$requiredDirs = @(
    "backend",
    "backend/app",
    "frontend",
    "frontend/pages",
    "frontend/components",
    "frontend/lib"
)

$dirOk = $true
foreach ($dir in $requiredDirs) {
    if (-not (Test-Path "d:\桌面\AI\$dir")) {
        $dirOk = $false
        break
    }
}

if ($dirOk) {
    Write-Host " ✅" -ForegroundColor Green
    $passed++
} else {
    Write-Host " ❌" -ForegroundColor Red
    $failed++
}
Write-Host ""

# 检查文件
Write-Host "[检查] 关键文件..." -ForegroundColor Yellow -NoNewline
$requiredFiles = @(
    "backend/requirements.txt",
    "backend/.env",
    "frontend/package.json",
    "frontend/.env.local"
)

$filesOk = $true
foreach ($file in $requiredFiles) {
    if (-not (Test-Path "d:\桌面\AI\$file")) {
        $filesOk = $false
        Write-Host " ❌ 缺失: $file" -ForegroundColor Red
        break
    }
}

if ($filesOk) {
    Write-Host " ✅" -ForegroundColor Green
    $passed++
} else {
    Write-Host " ❌" -ForegroundColor Red
    $failed++
}
Write-Host ""

# 摘要
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  检查摘要                               ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "  ✅ 通过: $passed" -ForegroundColor Green
Write-Host "  ❌ 失败: $failed" -ForegroundColor Red
Write-Host "  ⚠️  警告: $warnings" -ForegroundColor Yellow
Write-Host ""

if ($failed -eq 0) {
    Write-Host "  📌 所有必需环境检查通过！" -ForegroundColor Green
    Write-Host ""
    Write-Host "  下一步:" -ForegroundColor Cyan
    Write-Host "    1. 确保 PostgreSQL 运行（本地或 Docker）" -ForegroundColor Gray
    Write-Host "    2. 运行启动脚本: .\启动.ps1" -ForegroundColor Gray
    Write-Host "    3. 访问 http://localhost:3000" -ForegroundColor Gray
} else {
    Write-Host "  ⚠️  检查失败，请安装缺失的组件" -ForegroundColor Red
    Write-Host ""
    Write-Host "  必需组件:" -ForegroundColor Yellow
    Write-Host "    - Python 3.8+: https://www.python.org/" -ForegroundColor Gray
    Write-Host "    - Node.js 16+: https://nodejs.org/" -ForegroundColor Gray
}

Write-Host "`n按任意键继续..." -ForegroundColor Gray
$null = Read-Host
