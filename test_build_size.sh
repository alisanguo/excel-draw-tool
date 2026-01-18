#!/bin/bash

echo "======================================"
echo "打包大小测试"
echo "======================================"
echo ""

# 检查PyInstaller
if ! python -c "import PyInstaller" 2>/dev/null; then
    echo "正在安装PyInstaller..."
    pip install pyinstaller
fi

# 清理旧构建
echo "1. 清理旧构建..."
rm -rf build/ dist/
echo "   ✅ 清理完成"
echo ""

# 构建
echo "2. 开始构建..."
echo "   使用配置: build.spec"
source venv/bin/activate
pyinstaller --clean --noconfirm build.spec

if [ $? -ne 0 ]; then
    echo "   ❌ 构建失败"
    exit 1
fi

echo "   ✅ 构建完成"
echo ""

# 检查大小
echo "3. 文件大小统计"
echo "   =================================================="
echo ""

if [ -d "dist/excel-draw-tool" ]; then
    # 总体积
    TOTAL_SIZE=$(du -sh dist/excel-draw-tool | awk '{print $1}')
    echo "   📦 总大小: $TOTAL_SIZE"
    echo ""
    
    # 主要文件大小
    echo "   主要文件:"
    if [ -f "dist/excel-draw-tool/excel-draw-tool" ]; then
        ls -lh dist/excel-draw-tool/excel-draw-tool | awk '{print "     - 可执行文件:", $5}'
    fi
    
    if [ -d "dist/excel-draw-tool/static" ]; then
        du -sh dist/excel-draw-tool/static | awk '{print "     - static目录:", $1}'
    fi
    
    if [ -d "dist/excel-draw-tool/templates" ]; then
        du -sh dist/excel-draw-tool/templates | awk '{print "     - templates目录:", $1}'
    fi
    
    # 统计Python库大小
    echo ""
    echo "   主要依赖库:"
    if [ -d "dist/excel-draw-tool/_internal" ]; then
        cd dist/excel-draw-tool/_internal
        for lib in pandas numpy openpyxl flask werkzeug; do
            SIZE=$(du -sh $lib* 2>/dev/null | head -1 | awk '{print $1}')
            if [ ! -z "$SIZE" ]; then
                echo "     - $lib: $SIZE"
            fi
        done
        cd ../../..
    fi
    
    echo ""
    echo "   =================================================="
    
    # 详细文件列表（前20个最大的文件）
    echo ""
    echo "   前20个最大文件:"
    find dist/excel-draw-tool -type f -exec ls -lh {} \; | sort -k5 -hr | head -20 | awk '{print "     "$9, "-", $5}'
    
    echo ""
    echo "   =================================================="
    
    # 创建压缩包测试
    echo ""
    echo "4. 测试压缩大小..."
    cd dist
    tar -czf excel-draw-tool-test.tar.gz excel-draw-tool/
    COMPRESSED_SIZE=$(ls -lh excel-draw-tool-test.tar.gz | awk '{print $5}')
    echo "   📦 压缩后大小 (tar.gz): $COMPRESSED_SIZE"
    
    # 清理测试压缩包
    rm excel-draw-tool-test.tar.gz
    cd ..
    
else
    echo "   ❌ 构建目录不存在"
    exit 1
fi

echo ""
echo "======================================"
echo "5. 优化建议"
echo "======================================"
echo ""

# 分析并给出建议
TOTAL_MB=$(du -sm dist/excel-draw-tool | awk '{print $1}')

if [ $TOTAL_MB -gt 100 ]; then
    echo "   ⚠️  当前大小 ${TOTAL_MB}MB 较大，建议："
    echo "     - 检查是否包含了不必要的库"
    echo "     - 确认excludes配置已生效"
    echo "     - 考虑使用单文件模式"
elif [ $TOTAL_MB -gt 50 ]; then
    echo "   ✅ 当前大小 ${TOTAL_MB}MB 适中"
    echo "     - 可以进一步优化"
    echo "     - 检查大文件列表"
else
    echo "   🎉 当前大小 ${TOTAL_MB}MB 已优化良好！"
fi

echo ""
echo "6. 功能测试"
echo "======================================"
echo ""
echo "   请运行以下命令测试构建的程序："
echo ""
echo "   cd dist/excel-draw-tool"
echo "   ./excel-draw-tool"
echo ""
echo "   然后在浏览器访问 http://localhost:5000"
echo ""

