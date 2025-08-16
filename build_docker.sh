#!/bin/bash

echo "========================================"
echo "PreTools Android APK Builder (Docker)"
echo "========================================"

# 출력 디렉토리 생성
mkdir -p output

echo "Building Docker image..."
docker build -t pretools-builder .

if [ $? -ne 0 ]; then
    echo "Docker build failed!"
    exit 1
fi

echo "Building Android APK..."
docker run --rm -v "$(pwd)/output:/app/output" pretools-builder

if [ $? -ne 0 ]; then
    echo "APK build failed!"
    exit 1
fi

echo "========================================"
echo "Build completed!"
echo "APK location: output/"
echo "========================================"

ls -la output/*.apk 2>/dev/null || echo "No APK files found in output/"