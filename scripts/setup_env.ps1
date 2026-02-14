# LLM Folder Organizer - 环境配置向导 (Windows)
Write-Host "🔧 LLM Folder Organizer - 环境配置向导" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否已存在 .env 文件
if (Test-Path .env) {
    Write-Host "⚠️  发现已存在的 .env 文件" -ForegroundColor Yellow
    $overwrite = Read-Host "是否覆盖？(y/N)"
    if ($overwrite -notmatch '^[Yy]$') {
        Write-Host "❌ 已取消" -ForegroundColor Red
        exit 0
    }
    Write-Host ""
}

# 复制模板
if (-not (Test-Path .env.example)) {
    Write-Host "❌ 错误：找不到 .env.example 文件" -ForegroundColor Red
    exit 1
}

Copy-Item .env.example .env
Write-Host "✅ 已创建 .env 文件" -ForegroundColor Green
Write-Host ""

# 交互式配置 API Key
Write-Host "📝 请配置您的 API 密钥：" -ForegroundColor Cyan
Write-Host ""

$api_key = Read-Host "请输入 DEEPSEEK_API_KEY（必填）"
if ([string]::IsNullOrWhiteSpace($api_key)) {
    Write-Host "❌ 错误：DEEPSEEK_API_KEY 不能为空" -ForegroundColor Red
    Remove-Item .env
    exit 1
}

# 更新 .env ���件
$content = Get-Content .env
$content = $content -replace 'DEEPSEEK_API_KEY=.*', "DEEPSEEK_API_KEY=$api_key"
$content | Set-Content .env

Write-Host ""
Write-Host "可选配置（直接回车跳过）：" -ForegroundColor Cyan
Write-Host ""

# 可选：Base URL
$base_url = Read-Host "DEEPSEEK_BASE_URL (默认: https://api.deepseek.com)"
if (-not [string]::IsNullOrWhiteSpace($base_url)) {
    Add-Content .env "`nDEEPSEEK_BASE_URL=$base_url"
}

# 可选：Model
$model = Read-Host "DEEPSEEK_MODEL (默认: deepseek-chat)"
if (-not [string]::IsNullOrWhiteSpace($model)) {
    Add-Content .env "DEEPSEEK_MODEL=$model"
}

# 可选：WebUI 配置
$host_addr = Read-Host "LFO_HOST (默认: 127.0.0.1)"
if (-not [string]::IsNullOrWhiteSpace($host_addr)) {
    Add-Content .env "LFO_HOST=$host_addr"
}

$port = Read-Host "LFO_PORT (默认: 8501)"
if (-not [string]::IsNullOrWhiteSpace($port)) {
    Add-Content .env "LFO_PORT=$port"
}

Write-Host ""
Write-Host "✅ 配置完成！" -ForegroundColor Green
Write-Host ""
Write-Host "📄 你的 .env 文件已创建，内容如下：" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Get-Content .env | Write-Host
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 现在可以运行：" -ForegroundColor Green
Write-Host "   # PowerShell 方式加载环境变量："
Write-Host "   Get-Content .env | ForEach-Object { if (`$_ -match '^([^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable(`$matches[1], `$matches[2]) } }"
Write-Host "   lfo scan C:\path\to\folder"
Write-Host ""
Write-Host "🔒 安全提示：" -ForegroundColor Yellow
Write-Host "   .env 文件已自动加入 .gitignore，不会被提交到 Git"