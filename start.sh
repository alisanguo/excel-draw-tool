#!/bin/bash

echo "======================================"
echo "Excel缺陷数据统计分析工具"
echo "======================================"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 虚拟环境目录
VENV_DIR="venv"

# 创建虚拟环境（如果不存在）
if [ ! -d "$VENV_DIR" ]; then
    echo "正在创建虚拟环境..."
    python3 -m venv "$VENV_DIR"
    echo "虚拟环境创建完成"
    echo ""
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source "$VENV_DIR/bin/activate"

# 检查是否已安装依赖
if ! python -c "import flask" 2>/dev/null; then
    echo "正在安装依赖..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "依赖安装完成"
    echo ""
fi

echo "启动Web服务器..."
echo "访问地址: http://localhost:5000"
echo "按 Ctrl+C 停止服务"
echo ""

# 在虚拟环境中运行应用
python app.py

