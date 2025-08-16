@echo off
echo ========================================
echo PreTools Android APK Builder (Docker)
echo ========================================

REM 출력 디렉토리 생성
if not exist "output" mkdir output

echo Building Docker image...
docker build -t pretools-builder .

if %ERRORLEVEL% NEQ 0 (
    echo Docker build failed!
    pause
    exit /b 1
)

echo Building Android APK...
docker run --rm -v "%cd%\output:/app/output" pretools-builder

if %ERRORLEVEL% NEQ 0 (
    echo APK build failed!
    pause
    exit /b 1
)

echo ========================================
echo Build completed!
echo APK location: output\
echo ========================================

dir output\*.apk
pause