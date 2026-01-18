@echo off
chcp 65001 >nul
echo ============================================
echo Excel缺陷数据统计分析工具
echo ============================================
echo.
echo 启动中，请稍候...
echo.

REM 检查是否在打包后的目录
if exist "excel-draw-tool.exe" (
    echo 运行可执行文件...
    excel-draw-tool.exe
) else if exist "app.py" (
    echo 运行Python脚本...
    python app.py
) else (
    echo 错误: 找不到程序文件
    echo 请确保在正确的目录下运行此脚本
)

echo.
echo ============================================
echo 程序已退出
echo ============================================
echo.
pause

