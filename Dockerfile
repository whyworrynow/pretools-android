FROM ubuntu:20.04

# 환경변수 설정
ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/opt/android-sdk
ENV NDK_VERSION=20b
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    git \
    zip \
    unzip \
    openjdk-8-jdk \
    python3 \
    python3-pip \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
RUN pip3 install --upgrade pip
RUN pip3 install buildozer cython

# Android SDK 설치
RUN mkdir -p $ANDROID_HOME && \
    cd $ANDROID_HOME && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-6858069_latest.zip && \
    unzip -q commandlinetools-linux-6858069_latest.zip && \
    rm commandlinetools-linux-6858069_latest.zip && \
    yes | $ANDROID_HOME/cmdline-tools/bin/sdkmanager --sdk_root=$ANDROID_HOME "platform-tools" "platforms;android-30" "build-tools;30.0.3"

ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/bin:$ANDROID_HOME/platform-tools

# 작업 디렉토리 설정
WORKDIR /app

# buildozer 초기화를 위한 기본 파일들 복사
COPY buildozer.spec .
COPY overlay_style_app.py .
COPY icon.png .
COPY requirements.txt .

# buildozer 글로벌 디렉토리 생성
RUN mkdir -p /.buildozer

# APK 빌드
CMD ["sh", "-c", "buildozer android debug && cp bin/*.apk /app/output/"]