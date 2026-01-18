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

# 检查是否已安装依赖
if ! python3 -c "import flask" 2>/dev/null; then
    echo "正在安装依赖..."
    pip3 install -r requirements.txt
    echo ""
fi

echo "启动Web服务器..."
echo "访问地址: http://localhost:5000"
echo "按 Ctrl+C 停止服务"
echo ""

python3 app.py

