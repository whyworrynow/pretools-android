# PreTools Android 📱

> Windows PreTools를 안드로이드로 포팅한 터치 기반 드로잉 앱

## ✨ 주요 기능

- 🎨 **전체화면 드로잉** - 스크린샷 위에 주석 그리기
- 🖊️ **터치 기반 도구** - 펜, 지우개, 색상 선택
- 🎯 **오버레이 스타일** - 원본과 유사한 플로팅 UI
- 💾 **자동 저장** - 편집된 이미지 저장 및 공유
- 🎨 **색상 팔레트** - 최근 사용 색상 자동 저장

## 📱 스크린샷

![PreTools Android Demo](demo_screenshot.png)

## 🚀 설치

### 방법 1: APK 다운로드 (권장)
1. [Releases](../../releases) 페이지 방문
2. 최신 버전의 APK 다운로드
3. 안드로이드 기기에 설치

### 방법 2: 직접 빌드
빌드 방법은 [BUILD_GUIDE.md](BUILD_GUIDE.md) 참조

## 🎮 사용법

1. **앱 실행** → 전체화면 모드로 시작
2. **터치로 그리기** → 화면을 손가락으로 터치
3. **도구 변경** → 하단 툴바의 🖊️ 펜, 🧹 지우개
4. **색상 선택** → 색상 버튼 또는 🎨 버튼
5. **저장** → 💾 버튼으로 이미지 저장
6. **종료** → 우상단 ❌ 버튼

## 🛠️ 기술 스택

- **Framework**: Kivy (Python)
- **Build**: Buildozer + Android SDK
- **Platform**: Android 5.0+ (API 21+)
- **Architecture**: ARM64, ARMv7

## 📋 권한

- `WRITE_EXTERNAL_STORAGE` - 이미지 저장
- `READ_EXTERNAL_STORAGE` - 파일 접근
- `SYSTEM_ALERT_WINDOW` - 오버레이 표시

## 🔄 버전 히스토리

### v1.0.0 (2025-08-16)
- ✅ 초기 안드로이드 포팅 완성
- ✅ 터치 기반 드로잉 구현
- ✅ 오버레이 스타일 UI
- ✅ 색상 팔레트 및 도구 선택
- ✅ 자동 빌드 파이프라인

## 🤝 기여

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이센스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 참조

## 🙏 감사

- 원본 Windows PreTools 개발자
- Kivy 커뮤니티
- Python-for-Android 프로젝트

---

<div align="center">

**[Download APK](../../releases) • [Build Guide](BUILD_GUIDE.md) • [Report Issues](../../issues)**

Made with ❤️ by Claude Code

</div>