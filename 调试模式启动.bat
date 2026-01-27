@echo off
chcp 65001 >nul
title Excel缺陷数据统计分析工具 - 调试模式
color 0A

echo ============================================
echo Excel缺陷数据统计分析工具 - 调试模式
echo ============================================
echo.
echo 此模式会显示详细的错误信息和日志
echo.
echo 正在启动...
echo.

REM 设置Python环境变量（如果有）
set PYTHONUNBUFFERED=1

REM 检查并运行
if exist "excel-draw-tool.exe" (
    echo [调试] 找到可执行文件: excel-draw-tool.exe
    echo [调试] 当前目录: %CD%
    echo [调试] 开始运行...
    echo.
    echo ============================================
    echo.
    
    REM 捕获错误代码
    excel-draw-tool.exe
    set ERRORCODE=%ERRORLEVEL%
    
    echo.
    echo ============================================
    echo.
    echo [调试] 程序退出，错误代码: %ERRORCODE%
    
    if %ERRORCODE% NEQ 0 (
        echo [错误] 程序异常退出
        echo.
        echo 可能的原因:
        echo   1. 端口被占用（默认5000）
        echo   2. 缺少必要的文件
        echo   3. 权限不足
        echo.
        echo 解决方案:
        echo   1. 查看 logs 目录下的日志文件
        echo   2. 关闭占用5000端口的程序
        echo   3. 以管理员身份运行
        echo   4. 检查防火墙设置
    ) else (
        echo [成功] 程序正常退出
    )
    
) else if exist "app.py" (
    echo [调试] 找到Python脚本: app.py
    echo [调试] 使用Python运行...
    python app.py
) else (
    echo [错误] 找不到程序文件
    echo [调试] 当前目录: %CD%
    echo [调试] 目录内容:
    dir /b
)

echo.
echo ============================================
echo 按任意键查看日志文件（如果存在）...
pause >nul

if exist "logs" (
    echo.
    echo 日志文件:
    dir /b /o-d logs\*.log 2>nul
    echo.
    echo 是否查看最新日志? (Y/N)
    set /p VIEWLOG=
    if /i "%VIEWLOG%"=="Y" (
        for /f "delims=" %%f in ('dir /b /o-d logs\*.log 2^>nul') do (
            echo.
            echo ============================================
            echo 日志内容: logs\%%f
            echo ============================================
            type "logs\%%f"
            goto :logshown
        )
        :logshown
    )
)

echo.
echo ============================================
echo 按任意键退出...
pause >nul



