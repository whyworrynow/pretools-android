# PreTools Android 빌드 가이드

## 📱 앱 설명
원본 Windows PreTools 프로그램을 안드로이드로 포팅한 버전입니다.
- 전체화면 오버레이 스타일 드로잉
- 터치 기반 펜/지우개 도구
- 색상 선택 및 저장 기능
- 스크린샷 + 주석 방식

## 🚀 빌드 방법

### 방법 1: GitHub Actions (권장)

1. **GitHub 레포지토리 생성**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/pretools-android.git
   git push -u origin main
   ```

2. **자동 빌드**
   - GitHub에 푸시하면 자동으로 APK 빌드
   - Actions 탭에서 빌드 진행상황 확인
   - 완료되면 Artifacts에서 APK 다운로드

3. **릴리즈 생성** (선택사항)
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
   - 태그 푸시시 자동으로 Release 생성

### 방법 2: Docker (로컬)

#### 전제조건
- Docker Desktop 설치
- 최소 8GB RAM 권장

#### Windows
```cmd
build_docker.bat
```

#### Linux/Mac
```bash
./build_docker.sh
```

#### 수동 Docker 실행
```bash
# 이미지 빌드
docker build -t pretools-builder .

# APK 생성
mkdir output
docker run --rm -v "$(pwd)/output:/app/output" pretools-builder

# 결과 확인
ls output/*.apk
```

### 방법 3: Linux 환경에서 직접 빌드

#### 전제조건
```bash
sudo apt-get update
sudo apt-get install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

#### 빌드 실행
```bash
pip3 install buildozer
buildozer android debug
```

## 📦 빌드 결과

### 생성되는 파일
- `bin/pretools-1.0-arm64-v8a-debug.apk` - ARM64용 APK
- `bin/pretools-1.0-armeabi-v7a-debug.apk` - ARM32용 APK

### APK 설치
```bash
# Android 기기에 설치
adb install bin/*.apk

# 또는 APK 파일을 기기로 전송 후 수동 설치
```

## ⚙️ 설정 옵션

### buildozer.spec 주요 설정
```ini
# 앱 정보
title = PreTools
package.name = pretools
package.domain = com.pretools

# 아이콘 및 스플래시
icon.filename = icon.png
presplash.filename = icon.png

# 권한
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,SYSTEM_ALERT_WINDOW

# 메인 파일
source.main = overlay_style_app.py
```

### 의존성 패키지
```
kivy==2.1.0
android
pyjnius
plyer
pillow
```

## 🐛 트러블슈팅

### 빌드 실패시
1. **메모리 부족**
   - Docker Desktop 메모리 할당 증가 (8GB+)
   - 빌드 중 다른 프로그램 종료

2. **권한 오류**
   - Linux: `sudo` 없이 실행
   - Windows: 관리자 권한으로 실행

3. **네트워크 오류**
   - 안정적인 인터넷 연결 필요
   - 방화벽/백신 일시 해제

### 실행 오류시
1. **앱이 실행되지 않음**
   - Android 버전 확인 (최소 API 21+)
   - 개발자 옵션에서 "알 수 없는 소스" 허용

2. **권한 오류**
   - 앱 설정에서 저장소 권한 허용
   - "다른 앱 위에 그리기" 권한 허용

## 📖 사용법

1. **앱 실행** - 전체화면 모드로 시작
2. **드로잉** - 화면을 터치하여 그리기
3. **도구 변경** - 하단 툴바에서 펜/지우개 선택
4. **색상 변경** - 색상 버튼 또는 🎨 버튼
5. **저장** - 💾 버튼으로 이미지 저장
6. **종료** - 우상단 ❌ 버튼

## 📝 버전 히스토리

### v1.0.0 (2025-08-16)
- 초기 안드로이드 포팅 버전
- 오버레이 스타일 UI 구현
- 기본 드로잉 기능 완성
- 터치 기반 인터페이스 최적화