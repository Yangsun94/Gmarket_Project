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
│       └── test.yml              # GitHub Actions workflow
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

`.env` 파일을 생성하고 다음 내용을 입력:

```env
TEST_ID=your_gmarket_id
TEST_PASSWORD=your_gmarket_password
HEADLESS=true
```

## 💻 사용 방법

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

### 헤드리스 모드

```bash
# .env 파일에서 HEADLESS=true로 설정하거나
HEADLESS=true pytest tests/ -v
```

## 🔄 CI/CD

GitHub Actions를 통한 자동화 테스트가 구성되어 있습니다.

### 자동 실행 조건

- **Push**: `main`, `develop` 브랜치에 코드 푸시
- **Pull Request**: `main`, `develop` 브랜치로 PR 생성
- **Schedule**: 매일 오전 9시(KST) 자동 실행
- **Manual**: GitHub Actions 탭에서 수동 실행

### 수동 실행 방법

1. GitHub 저장소 → **Actions** 탭
2. **Gmarket Automation Tests** 선택
3. **Run workflow** 클릭
4. 테스트 타입 선택:
   - `all`: 모든 테스트
   - `integration`: 통합 테스트
   - `unit`: 단위 테스트
   - `login`: 로그인 테스트

### GitHub Secrets 설정

CI/CD가 작동하려면 다음 Secrets를 설정해야 합니다:

**Settings → Secrets and variables → Actions → New repository secret**

| Secret           | 설명 |
|------------------|------|
| `TEST_ID`        | G마켓 테스트 계정 이메일 |
| `TEST_PASSWORD`  | G마켓 테스트 계정 비밀번호 |
| `NAVER_EMAIL`    | 알림 받을 네이버 이메일 |
| `NAVER_PASSWORD` | 네이버 앱 비밀번호 ([발급 방법](https://nid.naver.com/user2/help/myInfoApp.nhn?lang=ko_KR)) |

### 테스트 리포트 확인

1. Actions 탭 → 실행된 workflow 클릭
2. **Artifacts** 섹션에서 `test-report-python-X.XX` 다운로드
3. `report.html` 파일을 브라우저로 열기

## 🏷️ 테스트 마커

`pytest.ini`에 정의된 마커를 사용하여 특정 테스트만 실행할 수 있습니다:

```bash
pytest -m smoke          # 스모크 테스트
pytest -m regression     # 회귀 테스트
pytest -m integration    # 통합 테스트
pytest -m login          # 로그인 테스트
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