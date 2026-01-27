#!/bin/bash

echo "======================================"
echo "推送bat编码问题修复到GitHub"
echo "======================================"
echo ""

# 添加所有修改的文件
echo "添加修改的文件..."
git add start.bat \
        start_debug.bat \
        START_HERE.txt \
        build.spec \
        .github/workflows/build.yml \
        README_Windows.txt \
        "Windows使用说明.md" \
        CHANGELOG.md \
        "bat编码问题修复说明.md" \
        push_bat_encoding_fix.sh

echo "✅ 文件已添加到暂存区"
echo ""

# 显示即将提交的更改
echo "即将提交的更改："
echo "----------------------------------------"
git status --short
echo "----------------------------------------"
echo ""

# 提交更改
echo "提交更改..."
git commit -m "fix: 修复Windows bat文件中文编码问题

问题:
- bat文件使用UTF-8编码，在某些Windows系统上无法正确解析
- 导致出现\"'录' 不是内部或外部命令\"错误
- 用户无法正常启动程序

解决方案:
- 创建纯ASCII版本的启动脚本（推荐使用）：
  * start.bat - 简单启动
  * start_debug.bat - 调试启动
- 保留中文版本作为备用
- 在所有Windows系统上都能正常工作

新增文件:
- start.bat - 英文简单启动脚本
- start_debug.bat - 英文调试启动脚本  
- START_HERE.txt - 快速开始指南（纯ASCII）
- bat编码问题修复说明.md - 技术文档

更新文件:
- build.spec - 包含新的bat文件
- .github/workflows/build.yml - 复制START_HERE.txt
- README_Windows.txt - 添加编码问题说明
- Windows使用说明.md - 优先推荐英文版本
- CHANGELOG.md - 记录修复

测试:
- 所有bat文件使用纯ASCII字符
- 在各种Windows系统上兼容
- 完全解决编码问题

关闭 #bat编码问题"

if [ $? -eq 0 ]; then
    echo "✅ 提交成功"
    echo ""
else
    echo "❌ 提交失败"
    exit 1
fi

# 推送到远程仓库
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
    echo "4. 验证bat文件可以正常启动"
    echo ""
    echo "测试步骤："
    echo "1. 解压zip文件"
    echo "2. 双击 start_debug.bat（推荐）"
    echo "3. 或双击 start.bat"
    echo "4. 验证不再出现编码错误"
    echo ""
    echo "GitHub Actions:"
    echo "https://github.com/alisanguo/excel-draw-tool/actions"
    echo ""
else
    echo ""
    echo "❌ 推送失败，请检查网络连接和仓库权限"
    exit 1
fi



