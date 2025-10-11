# 🛒 G마켓 자동화 테스트 프로젝트

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.48.0-green)](https://playwright.dev/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Playwright를 활용한 G마켓 쇼핑몰 E2E 자동화 테스트 프레임워크입니다.

## 📋 목차

- [프로젝트 소개](#-프로젝트-소개)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [설치 방법](#-설치-방법)
- [사용 방법](#-사용-방법)
- [테스트 실행](#-테스트-실행)
- [CI/CD](#-cicd)
- [코드 품질](#-코드-품질)
- [학습 내용](#-학습-내용)

## 🎯 프로젝트 소개

이 프로젝트는 G마켓 쇼핑몰의 주요 기능을 자동으로 테스트하는 E2E(End-to-End) 테스트 프레임워크입니다. Page Object Model 패턴을 적용하여 유지보수성과 재사용성을 높였으며, pytest를 기반으로 체계적인 테스트 환경을 구축했습니다.

### 🎓 학습 목표

- **Playwright**를 활용한 웹 자동화 테스트 구현
- **Page Object Model** 디자인 패턴 적용
- **단위 테스트 / 통합 테스트** 작성
- **GitHub Actions**를 통한 CI/CD 파이프라인 구축
- **코드 품질 관리** 자동화 (Black, isort, Flake8, Pylint)

## ✨ 주요 기능

### 테스트 범위

- ✅ **홈페이지**: 방문, 로고 클릭, 검색 기능
- ✅ **검색 페이지**: 상품 검색, 필터링, 정렬, 상품 클릭
- ✅ **상품 상세 페이지**: 상품 정보 조회, 장바구니 담기
- ✅ **장바구니**: 상품 확인, 수량 변경, 삭제
- ✅ **로그인/로그아웃**: 인증 플로우

### 특징

- 🤖 **봇 탐지 우회**: 자연스러운 사용자 행동 시뮬레이션
- 📸 **자동 스크린샷**: 테스트 실패 시 자동 캡처
- 📊 **HTML 리포트**: 테스트 결과 시각화
- 🔄 **재사용 가능한 구조**: Page Object Model 패턴
- 🧪 **단위/통합 테스트**: 계층적 테스트 구조

## 🛠 기술 스택

### Core
- **Python 3.10+**: 메인 언어
- **Playwright 1.48.0**: 웹 자동화 라이브러리
- **pytest 8.3.3**: 테스트 프레임워크

### Testing
- **pytest-html**: HTML 테스트 리포트 생성

### Code Quality
- **Black**: 코드 포맷터
- **isort**: Import 정렬
- **Flake8**: 린터 (PEP 8 검사)
- **Pylint**: 정적 코드 분석
- **pre-commit**: Git hook 자동화

### CI/CD
- **GitHub Actions**: 자동화 워크플로우
- **Safety**: 보안 취약점 검사

## 📁 프로젝트 구조

```
gmarket-automation/
├── .github/
│   └── workflows/
│       └── quality-check.yml    # CI/CD 파이프라인
├── framework/
│   ├── base/
│   │   └── base_page.py         # 모든 페이지의 베이스 클래스
│   ├── config/
│   │   └── locators.py          # 모든 페이지 Locator 정의
│   └── pages/
│       ├── home_page.py         # 홈페이지
│       ├── search_page.py       # 검색 페이지
│       ├── product_page.py      # 상품 상세 페이지
│       ├── cart_page.py         # 장바구니 페이지
│       └── login_page.py        # 로그인 페이지
├── tests/
│   ├── test_integration.py      # 통합 테스트 (E2E)
│   ├── test_homepage.py         # HomePage 단위 테스트
│   ├── test_searchpage.py       # SearchPage 단위 테스트
│   ├── test_productpage.py      # ProductPage 단위 테스트
│   └── test_cartpage.py         # CartPage 단위 테스트
├── reports/                     # 테스트 리포트 저장 폴더
├── .env                         # 환경 변수 (git 제외)
├── .env.example                 # 환경 변수 예시
├── .gitignore                   # Git 제외 파일
├── .pre-commit-config.yaml      # pre-commit 설정
├── conftest.py                  # pytest 설정 및 fixture
├── pytest.ini                   # pytest 옵션 설정
├── requirements.txt             # 프로젝트 의존성
└── README.md                    # 프로젝트 문서
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

### 3. 의존성 설치

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. 환경 변수 설정

`.env.example`을 복사하여 `.env` 파일을 생성하고 계정 정보를 입력합니다:

```bash
cp .env.example .env
```

`.env` 파일 예시:
```env
TEST_ID=your_gmarket_id
TEST_PASSWORD=your_gmarket_password
```

### 5. pre-commit 설치

```bash
pre-commit install
```

## 🧪 테스트 실행

### 전체 테스트 실행

```bash
pytest tests/ -v
```

### 단위 테스트만 실행

```bash
pytest tests/test_homepage.py tests/test_searchpage.py tests/test_productpage.py tests/test_cartpage.py -v
```

### 통합 테스트만 실행

```bash
pytest tests/test_integration.py -v
```

### 특정 마커로 실행

```bash
# 로그인 테스트만
pytest tests/ -m login -v

# 장바구니 테스트만
pytest tests/ -m cart -v

# 느린 테스트 제외
pytest tests/ -m "not slow" -v
```

### HTML 리포트 생성

```bash
pytest tests/ --html=reports/report.html --self-contained-html
```

## 🔄 CI/CD

### GitHub Actions

이 프로젝트는 GitHub Actions를 통해 자동화된 코드 품질 검사를 수행합니다.

> G마켓의 강력한 봇 탐지 시스템으로 인해 CI/CD 환경에서는 E2E 테스트 대신 **코드 품질 검사**를 수행합니다.

### 자동 실행 조건

- **Push**: `main`, `develop` 브랜치에 코드 푸시 시
- **Pull Request**: `main`, `develop` 브랜치로 PR 생성 시
- **Manual**: GitHub Actions 탭에서 수동 실행 가능

### 검사 항목

#### 코드 품질 검사
- **Flake8**: PEP 8 스타일 가이드 준수 확인
- **Black**: 코드 포맷팅 일관성 검사
- **Pylint**: 상세한 코드 품질 분석
- **isort**: Import 문 정렬 확인

#### 보안 검사
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

## ✅ 코드 품질

### 로컬에서 코드 품질 검사

```bash
# 1. Black: 코드 포맷팅
black framework/ tests/ --line-length=120

# 2. isort: Import 정렬
isort framework/ tests/ --profile black

# 3. Flake8: 스타일 검사
flake8 framework/ tests/ --max-line-length=120 --extend-ignore=E203,W503

# 4. Pylint: 정적 분석
pylint framework/ --fail-under=7.0

# 5. Safety: 보안 검사
safety check
```

### pre-commit 사용

Git commit 시 자동으로 코드 품질 검사가 실행됩니다:

```bash
git add .
git commit -m "feat: 새 기능 추가"
# → Black, isort, Flake8가 자동 실행됨
```

전체 파일 검사:

```bash
pre-commit run --all-files
```

## 📚 학습 내용

이 프로젝트를 통해 다음을 학습했습니다:

### 1. 웹 자동화 테스트
- ✅ Playwright를 활용한 E2E 테스트 자동화
- ✅ Page Object Model 디자인 패턴 적용
- ✅ 봇 탐지 우회 기법 (자연스러운 딜레이, 랜덤 타이핑)

### 2. 테스트 설계
- ✅ 단위 테스트와 통합 테스트 분리
- ✅ pytest fixture를 활용한 테스트 격리
- ✅ 테스트 마커를 통한 선택적 실행

### 3. CI/CD 파이프라인
- ✅ GitHub Actions 워크플로우 구축
- ✅ 코드 품질 자동화 검증
- ✅ 실무 제약사항 이해 및 대안 마련

### 4. 코드 품질 관리
- ✅ Black, isort를 통한 일관된 코드 스타일 유지
- ✅ Flake8, Pylint를 통한 코드 품질 검증
- ✅ pre-commit hooks를 통한 자동화