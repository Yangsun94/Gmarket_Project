# 🛒 G마켓 자동화 테스트 프로젝트

Playwright와 Pytest를 활용한 G마켓 E-commerce 웹 자동화 테스트 프레임워크

[![Tests](https://github.com/YOUR_USERNAME/gmarket-automation/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_USERNAME/gmarket-automation/actions)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.48.0-green)](https://playwright.dev/)

## 📋 목차

- [프로젝트 소개](#-프로젝트-소개)
- [주요 기능](#-주요-기능)
- [프로젝트 구조](#-프로젝트-구조)
- [설치 방법](#-설치-방법)
- [사용 방법](#-사용-방법)
- [CI/CD](#-cicd)
- [테스트 마커](#-테스트-마커)
- [기여 방법](#-기여-방법)

## 🎯 프로젝트 소개

이 프로젝트는 G마켓 웹사이트의 주요 기능을 자동화 테스트하는 프레임워크입니다. Page Object Model(POM) 디자인 패턴을 적용하여 유지보수성과 확장성을 높였습니다.

### 테스트 범위
- 🏠 홈페이지 검색 기능
- 🔍 상품 검색 및 필터링
- 📦 상품 상세 정보 조회
- 🛒 장바구니 CRUD 기능
- 🔐 로그인/로그아웃

## ✨ 주요 기능

- **Page Object Model (POM)**: 유지보수가 쉬운 구조
- **봇 탐지 우회**: 자연스러운 사용자 행동 시뮬레이션
- **자동 스크린샷**: 테스트 실패 시 자동 캡처
- **HTML 리포트**: 시각적인 테스트 결과 확인
- **CI/CD 파이프라인**: GitHub Actions 자동화
- **이메일 알림**: 테스트 실패 시 네이버 메일 알림

## 📁 프로젝트 구조

```
gmarket-automation/
├── .github/
│   └── workflows/
│       └── quality-check.yml             # GitHub Actions workflow
├── framework/
│   ├── base/
│   │   └── base_page.py          # 모든 페이지의 베이스 클래스
│   ├── config/
│   │   └── locators.py           # Locator 정의
│   └── pages/
│       ├── home_page.py          # 홈페이지
│       ├── search_page.py        # 검색 결과 페이지
│       ├── product_page.py       # 상품 상세 페이지
│       ├── cart_page.py          # 장바구니 페이지
│       └── login_page.py         # 로그인 페이지
├── tests/
│   ├── integration/
│   │   └── test_integration.py   # 통합 테스트
│   └── unit/
│       ├── test_homepage.py      # 홈페이지 단위 테스트
│       ├── test_searchpage.py    # 검색 페이지 단위 테스트
│       └── test_productpage.py   # 상품 페이지 단위 테스트
├── screenshots/                   # 실패 시 스크린샷 저장
├── .env                          # 환경 변수 (git에서 제외)
├── .gitignore
├── conftest.py                   # pytest 설정 및 fixtures
├── pytest.ini                    # pytest 옵션 및 마커
├── requirements.txt              # Python 의존성
└── README.md
```

## 🚀 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/Yangsun94/Gmarket_Project.git
cd gmarket-automation
```

### 2. 가상환경 생성 및 활성화

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. 환경 변수 설정

`.env` 파일을 생성하고 **본인의 실제 계정 정보**를 입력:

```env
TEST_ID=본인의_G마켓_ID
TEST_PASSWORD=본인의_G마켓_비밀번호
```

> ⚠️ **주의**: `.env` 파일은 `.gitignore`에 포함되어 GitHub에 업로드되지 않습니다.

**선택사항**: 헤드리스 모드로 실행하려면 추가:

```env
HEADLESS=true
```

> 💡 **헤드리스 모드**: 브라우저 창 없이 백그라운드에서 테스트 실행 (빠르고 리소스 절약)

### 전체 테스트 실행

```bash
pytest tests/ -v
```

### 특정 테스트 타입 실행

```bash
# 통합 테스트만
pytest tests/integration/ -v

# 단위 테스트만
pytest tests/unit/ -v

# 로그인 테스트만
pytest tests/ -m login -v
```

### HTML 리포트 생성

```bash
pytest tests/ -v --html=report.html --self-contained-html
```

### 헤드리스 모드 (선택사항)

브라우저 창 없이 백그라운드에서 실행:

```bash
# 방법 1: .env 파일에 추가
HEADLESS=true

# 방법 2: 환경 변수로 직접 실행
HEADLESS=true pytest tests/ -v
```

## 🔄 CI/CD

### ⚠️ E2E 테스트 자동화 시도 및 전환

**초기 목표:** Playwright를 활용한 E2E 테스트 자동화

**발견된 문제:** G마켓의 봇 탐지 시스템
- GitHub Actions 서버 IP 차단
- 헤드리스 모드 감지
- 로그인 및 대부분의 상호작용 차단

**해결 방법:** 코드 품질 자동 검사로 전환

GitHub Actions를 통한 **코드 품질 자동 검사**가 구성되어 있습니다.

### 자동 실행 조건

- **Push**: `main`, `develop` 브랜치에 코드 푸시 시
- **Pull Request**: `main`, `develop` 브랜치로 PR 생성 시
- **Manual**: GitHub Actions 탭에서 수동 실행 가능

### 검사 항목

#### **코드 품질 검사**
- **Flake8**: PEP 8 스타일 가이드 준수 확인
- **Black**: 코드 포맷팅 일관성 검사
- **Pylint**: 상세한 코드 품질 분석
- **isort**: Import 문 정렬 확인

#### **보안 검사**
- **Safety**: 알려진 보안 취약점 검사

### 로컬 테스트 실행

E2E 테스트는 로컬 환경에서만 실행 가능합니다:

```bash
# 전체 테스트
pytest tests/ -v

# 통합 테스트
pytest tests/integration/ -v

# 단위 테스트
pytest tests/unit/ -v

# 로그인 테스트
pytest tests/ -m login -v
```

### 학습 내용

이 프로젝트를 통해 다음을 학습했습니다:
- ✅ Playwright E2E 테스트 자동화 구현
- ✅ GitHub Actions CI/CD 파이프라인 구축
- ✅ 실무 제약사항 (봇 탐지) 이해 및 대안 마련
- ✅ 코드 품질 자동화 도구 활용

## 🏷️ 테스트 마커

`pytest.ini`에 정의된 마커를 사용하여 특정 테스트만 실행할 수 있습니다:

```bash
pytest -m smoke          # 스모크 테스트
pytest -m regression     # 회귀 테스트
pytest -m integration    # 통합 테스트
pytest -m login          # 로그인 테스트
pytest -m search         # 검색 테스트
pytest -m cart           # 장바구니 테스트
pytest -m slow           # 느린 테스트
```

### 마커 조합

```bash
# 로그인 테스트 제외
pytest -m "not login"

# 통합 테스트이면서 느리지 않은 테스트
pytest -m "integration and not slow"
```

## 🛠️ 개발 환경

- **Python**: 3.10, 3.11
- **Playwright**: 1.48.0
- **Pytest**: 8.3.3
- **IDE**: PyCharm (추천)

## 📊 테스트 커버리지

현재 구현된 테스트:

- ✅ 홈페이지 검색 기능
- ✅ 검색 결과 필터링 및 정렬
- ✅ 상품 상세 정보 조회
- ✅ 장바구니 추가/수정/삭제
- ✅ 로그인/로그아웃
- ❌ 결제 프로세스 (제외)
