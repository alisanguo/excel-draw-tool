#!/bin/bash

echo "======================================"
echo "离线功能测试"
echo "======================================"
echo ""

# 检查ECharts文件
echo "1. 检查ECharts本地文件..."
if [ -f "static/js/echarts.min.js" ]; then
    FILE_SIZE=$(ls -lh static/js/echarts.min.js | awk '{print $5}')
    echo "   ✅ ECharts文件存在: $FILE_SIZE"
else
    echo "   ❌ ECharts文件不存在"
    echo "   请运行以下命令下载："
    echo "   mkdir -p static/js"
    echo "   curl -o static/js/echarts.min.js https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"
    exit 1
fi

# 检查模板文件
echo ""
echo "2. 检查HTML模板..."
if grep -q "url_for('static'" templates/index.html; then
    echo "   ✅ HTML已更新为使用本地ECharts"
else
    echo "   ❌ HTML仍在使用CDN"
    exit 1
fi

# 检查build.spec
echo ""
echo "3. 检查PyInstaller配置..."
if grep -q "('static', 'static')" build.spec; then
    echo "   ✅ build.spec已配置打包static目录"
else
    echo "   ❌ build.spec未配置static目录"
    exit 1
fi

# 启动Flask测试
echo ""
echo "4. 启动Flask应用测试..."
echo "   启动服务器: http://localhost:5000"
echo "   请在浏览器中："
echo "   - 打开 http://localhost:5000"
echo "   - 打开浏览器开发者工具(F12)"
echo "   - 查看Console，应该显示: ECharts loaded successfully"
echo "   - 上传示例文件测试图表显示"
echo ""
echo "   按Ctrl+C停止服务器"
echo ""

source venv/bin/activate
python app.py



