@echo off
REM Excel Defect Data Analysis Tool - Launcher
REM This file uses only ASCII characters for maximum compatibility

echo ============================================
echo Excel Defect Data Analysis Tool
echo ============================================
echo.
echo Starting, please wait...
echo.

REM Check if executable exists
if exist "excel-draw-tool.exe" (
    echo Running executable...
    excel-draw-tool.exe
) else if exist "app.py" (
    echo Running Python script...
    python app.py
) else (
    echo ERROR: Program file not found
    echo Please run this script in the correct directory
)

echo.
echo ============================================
echo Program exited
echo ============================================
echo.
pause

