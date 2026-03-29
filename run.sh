#!/bin/bash
# 运行创业灵感简报
# 用法: ./run.sh
# 确保已配置 .env 文件（参考 .env.example）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 加载环境变量
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "❌ 未找到 .env 文件，请先复制 .env.example 并填入配置"
    exit 1
fi

# 激活虚拟环境（如果存在）
if [ -d venv ]; then
    source venv/bin/activate
fi

python main.py
