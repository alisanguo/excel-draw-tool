#!/bin/bash

echo "======================================"
echo "推送打包优化到GitHub"
echo "======================================"
echo ""

# 检查git仓库
if [ ! -d ".git" ]; then
    echo "❌ 未找到Git仓库"
    echo "请先运行: ./init_git.sh"
    exit 1
fi

echo "📊 优化总结："
echo ""
echo "  📦 预期效果:"
echo "     原大小: 150-200MB"
echo "     优化后: 50-80MB"
echo "     减少:   50-70%"
echo "     压缩后: 20-35MB"
echo ""
echo "  🎯 主要优化:"
echo "     ✓ 排除30+个不必要模块"
echo "     ✓ 启用strip移除调试符号"
echo "     ✓ 优化UPX压缩"
echo "     ✓ 最大压缩级别"
echo ""
echo "  📝 修改的文件:"
echo "     ✓ build.spec"
echo "     ✓ .github/workflows/build.yml"
echo "     ✓ 新增优化文档和测试脚本"
echo ""

read -p "是否继续推送？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "已取消"
    exit 1
fi

echo ""
echo "📦 添加文件..."
git add build.spec
git add .github/workflows/build.yml
git add 打包优化说明.md
git add test_build_size.sh
git add 优化总结.txt
git add CHANGELOG.md
git add requirements-build.txt

echo ""
echo "📝 提交优化..."
git commit -m "perf: 大幅优化打包配置，减小50-70%体积

🎯 优化措施
- 排除30+个不必要的Python模块（matplotlib, scipy等）
- 启用strip移除调试符号
- 优化UPX压缩配置
- 使用最大压缩级别
- 移除非必要文件

📊 预期效果
- 原大小: 150-200MB
- 优化后: 50-80MB
- 减少: 50-70%
- 压缩后: 20-35MB

📝 新增文件
- 打包优化说明.md - 详细优化文档
- test_build_size.sh - 本地大小测试脚本
- 优化总结.txt - 快速参考
- requirements-build.txt - 最小化构建依赖

🧪 验证
推送后查看GitHub Actions日志中的文件大小"

echo ""
echo "🚀 推送到GitHub..."
git push

echo ""
echo "======================================"
echo "✅ 推送完成！"
echo "======================================"
echo ""
echo "📊 下一步："
echo ""
echo "1. 查看GitHub Actions构建"
echo "   https://github.com/你的用户名/excel-draw-tool/actions"
echo ""
echo "2. 等待构建完成（约10分钟）"
echo ""
echo "3. 查看构建日志中的大小信息"
echo "   应该看到类似：Size of dist/excel-draw-tool: XX MB"
echo ""
echo "4. 下载artifacts验证"
echo "   - 检查文件大小"
echo "   - 测试功能是否正常"
echo ""
echo "📚 相关文档："
echo "   - 打包优化说明.md"
echo "   - 优化总结.txt"
echo ""
echo "🧪 本地测试："
echo "   ./test_build_size.sh"
echo ""

