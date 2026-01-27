#!/bin/bash

echo "======================================"
echo "初始化Git仓库并推送到GitHub"
echo "======================================"
echo ""

# 检查是否已有git仓库
if [ -d ".git" ]; then
    echo "Git仓库已存在"
else
    echo "初始化Git仓库..."
    git init
fi

echo ""
echo "添加所有文件..."
git add .

echo ""
echo "提交文件..."
git commit -m "Initial commit with GitHub Actions support"

echo ""
echo "======================================"
echo "请按照以下步骤完成："
echo "======================================"
echo ""
echo "1. 在GitHub上创建一个新仓库（不要初始化README）"
echo "   https://github.com/new"
echo ""
echo "2. 复制仓库URL，然后运行："
echo "   git remote add origin https://github.com/你的用户名/你的仓库名.git"
echo ""
echo "3. 推送到GitHub："
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. （可选）创建版本标签并推送："
echo "   git tag v1.0.0"
echo "   git push origin v1.0.0"
echo ""
echo "5. 在GitHub仓库的Actions页面查看自动构建进度"
echo ""
echo "详细说明请查看: GITHUB_DEPLOY.md"
echo ""



