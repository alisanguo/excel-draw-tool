@echo off
REM Excel Defect Data Analysis Tool - Debug Mode
REM This file uses only ASCII characters for maximum compatibility

title Excel Defect Data Analysis Tool - Debug Mode
color 0A

echo ============================================
echo Excel Defect Data Analysis Tool - Debug Mode
echo ============================================
echo.
echo This mode shows detailed error messages and logs
echo.
echo Starting...
echo.

REM Set Python environment (if needed)
set PYTHONUNBUFFERED=1

REM Check and run
if exist "excel-draw-tool.exe" (
    echo [DEBUG] Found executable: excel-draw-tool.exe
    echo [DEBUG] Current directory: %CD%
    echo [DEBUG] Starting...
    echo.
    echo ============================================
    echo.
    
    REM Capture error code
    excel-draw-tool.exe
    set ERRORCODE=%ERRORLEVEL%
    
    echo.
    echo ============================================
    echo.
    echo [DEBUG] Program exited with code: %ERRORCODE%
    
    if %ERRORCODE% NEQ 0 (
        echo [ERROR] Program exited abnormally
        echo.
        echo Possible causes:
        echo   1. Port 5000 is occupied
        echo   2. Missing required files
        echo   3. Insufficient permissions
        echo.
        echo Solutions:
        echo   1. Check logs directory for log files
        echo   2. Close programs using port 5000
        echo   3. Run as administrator
        echo   4. Check firewall settings
    ) else (
        echo [SUCCESS] Program exited normally
    )
    
) else if exist "app.py" (
    echo [DEBUG] Found Python script: app.py
    echo [DEBUG] Running with Python...
    python app.py
) else (
    echo [ERROR] Program file not found
    echo [DEBUG] Current directory: %CD%
    echo [DEBUG] Directory contents:
    dir /b
)

echo.
echo ============================================
echo Press any key to view log files (if exist)...
pause >nul

if exist "logs" (
    echo.
    echo Log files:
    dir /b /o-d logs\*.log 2>nul
    echo.
    echo View latest log? (Y/N)
    set /p VIEWLOG=
    if /i "%VIEWLOG%"=="Y" (
        for /f "delims=" %%f in ('dir /b /o-d logs\*.log 2^>nul') do (
            echo.
            echo ============================================
            echo Log content: logs\%%f
            echo ============================================
            type "logs\%%f"
            goto :logshown
        )
        :logshown
    )
)

echo.
echo ============================================
echo Press any key to exit...
pause >nul

