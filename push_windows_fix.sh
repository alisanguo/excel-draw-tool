#!/bin/bash

echo "======================================"
echo "推送Windows启动问题修复到GitHub"
echo "======================================"
echo ""

# 1. 运行测试
echo "步骤 1/3: 运行测试..."
python test_windows_fix.py
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 测试未通过，请检查并修复问题后再提交"
    exit 1
fi
echo ""

# 2. 添加所有修改的文件
echo "步骤 2/3: 添加修改的文件..."
git add app.py \
        启动.bat \
        调试模式启动.bat \
        Windows使用说明.md \
        README_Windows.txt \
        Windows问题修复说明.md \
        build.spec \
        .github/workflows/build.yml \
        test_windows_fix.py \
        CHANGELOG.md \
        push_windows_fix.sh

echo "✅ 文件已添加到暂存区"
echo ""

# 3. 显示即将提交的更改
echo "即将提交的更改："
echo "----------------------------------------"
git status --short
echo "----------------------------------------"
echo ""

# 4. 提交更改
echo "步骤 3/3: 提交更改..."
git commit -m "fix: 修复Windows版本窗口一闪而过的问题

主要修复:
- 增强错误处理和日志记录
- 自动端口检测和切换(5000-5009)
- 程序出错时暂停，显示详细信息
- 创建logs目录记录运行日志

新增启动脚本:
- 启动.bat - 普通启动
- 调试模式启动.bat - 调试模式（推荐）

完善文档:
- Windows使用说明.md
- README_Windows.txt
- Windows问题修复说明.md

优化构建:
- 更新build.spec包含bat文件
- 更新GitHub Actions复制文档到Windows构建
- 添加测试脚本验证修复

测试:
- 所有测试通过（5/5）
- 端口检查、日志创建、启动脚本、依赖导入、构建配置

关闭 #Windows启动问题"

if [ $? -eq 0 ]; then
    echo "✅ 提交成功"
    echo ""
else
    echo "❌ 提交失败"
    exit 1
fi

# 5. 推送到远程仓库
echo "推送到远程仓库..."
git push

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✅ 修复已成功推送到GitHub！"
    echo "======================================"
    echo ""
    echo "下一步："
    echo "1. 访问 GitHub Actions 查看构建状态"
    echo "2. 等待构建完成（约5-10分钟）"
    echo "3. 下载Windows版本测试"
    echo "4. 验证启动问题已修复"
    echo ""
    echo "快速链接："
    echo "- Actions: https://github.com/YOUR_USERNAME/excel-draw-tool/actions"
    echo "- Artifacts: 构建完成后在Actions页面下载"
    echo ""
else
    echo ""
    echo "❌ 推送失败，请检查网络连接和仓库权限"
    exit 1
fi



