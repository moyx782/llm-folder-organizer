#!/usr/bin/env bash
set -euo pipefail

echo "🔧 LLM Folder Organizer - 环境配置向导"
echo "========================================="
echo ""

# 检查是否已存在 .env 文件
if [ -f .env ]; then
    echo "⚠️  发现已存在的 .env 文件"
    read -p "是否覆盖？(y/N): " overwrite
    if [[ ! "$overwrite" =~ ^[Yy]$ ]]; then
        echo "❌ 已取消"
        exit 0
    fi
    echo ""
fi

# 复制模板
if [ ! -f .env.example ]; then
    echo "❌ 错误：找不到 .env.example 文件"
    exit 1
fi

cp .env.example .env
echo "✅ 已创建 .env 文件"
echo ""

# 交互式配置 API Key
echo "📝 请配置您的 API 密钥："
echo ""

read -p "请输入 DEEPSEEK_API_KEY（必填）: " api_key
if [ -z "$api_key" ]; then
    echo "❌ 错误：DEEPSEEK_API_KEY 不能为空"
    rm .env
    exit 1
fi

# 更新 .env 文件
sed -i.bak "s/DEEPSEEK_API_KEY=.*/DEEPSEEK_API_KEY=$api_key/" .env
rm .env.bak 2>/dev/null || true

echo ""
echo "可选配置（直接回车跳过）："
echo ""

# 可选：Base URL
read -p "DEEPSEEK_BASE_URL (默认: https://api.deepseek.com): " base_url
if [ -n "$base_url" ]; then
    echo "DEEPSEEK_BASE_URL=$base_url" >> .env
fi

# 可选：Model
read -p "DEEPSEEK_MODEL (默认: deepseek-chat): " model
if [ -n "$model" ]; then
    echo "DEEPSEEK_MODEL=$model" >> .env
fi

# 可选：WebUI 配置
read -p "LFO_HOST (默认: 127.0.0.1): " host
if [ -n "$host" ]; then
    echo "LFO_HOST=$host" >> .env
fi

read -p "LFO_PORT (默认: 8501): " port
if [ -n "$port" ]; then
    echo "LFO_PORT=$port" >> .env
fi

echo ""
echo "✅ 配置完成！"
echo ""
echo "📄 你的 .env 文件已创建，内容如下："
echo "========================================="
cat .env
echo "========================================="
echo ""
echo "🚀 现在可以运行："
echo "   source .env  # 或者 export \$(cat .env | xargs)"
echo "   lfo scan /path/to/folder"
echo ""
echo "🔒 安全提示："
echo "   .env 文件已自动加入 .gitignore，不会被提交到 Git"