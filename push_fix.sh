#!/bin/bash

echo "======================================"
echo "推送GitHub Actions修复"
echo "======================================"
echo ""

# 检查是否有git仓库
if [ ! -d ".git" ]; then
    echo "错误: 未找到Git仓库"
    echo "请先运行: ./init_git.sh"
    exit 1
fi

echo "添加修复文件..."
git add .github/workflows/build.yml
git add CHANGELOG.md
git add 修复说明.md

echo ""
echo "提交修复..."
git commit -m "fix: 更新GitHub Actions到最新版本，修复构建失败问题

- 更新 actions/upload-artifact v3 -> v4
- 更新 actions/setup-python v4 -> v5  
- 更新 softprops/action-gh-release v1 -> v2
- 解决 artifact actions v3 弃用问题"

echo ""
echo "推送到GitHub..."
git push

echo ""
echo "======================================"
echo "修复已推送！"
echo "======================================"
echo ""
echo "请访问GitHub仓库的Actions页面查看构建进度："
echo "https://github.com/你的用户名/excel-draw-tool/actions"
echo ""
echo "预计5-10分钟后构建完成"
echo ""

