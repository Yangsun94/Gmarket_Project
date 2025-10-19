"""
G마켓 자동화 테스트 공통 설정 파일

이 파일은 pytest의 설정과 공통 fixture들을 정의합니다.
- Browser/Context/Page fixture
- 봇 탐지 우회 설정
- 스크린샷 자동 저장
- 테스트 계정 정보 관리
"""

import os
from datetime import datetime

import pytest
import pytest_html
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()


# ==================== Browser Fixtures ====================


@pytest.fixture(scope="session")
def browser():
    """
    전체 테스트 세션 동안 하나의 브라우저 인스턴스를 공유합니다.

    봇 탐지 우회를 위한 설정:
    - --disable-blink-features=AutomationControlled
    - --disable-automation
    - webdriver 속성 제거
    """
    with sync_playwright() as p:
        headless = os.getenv("HEADLESS", "false").lower() == "true"

        # 🤖 봇 탐지 우회를 위한 브라우저 설정
        browser = p.chromium.launch(
            headless=headless,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--disable-automation",
                "--exclude-switches=enable-automation",
            ],
        )
        yield browser
        browser.close()


@pytest.fixture
def context(browser):
    """
    각 테스트마다 새로운 브라우저 컨텍스트를 생성합니다.

    - 한국어 로케일 및 타임존 설정
    - 자동화 감지 제거 스크립트 주입
    - 자연스러운 User-Agent 설정
    """

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080},
        locale="ko-KR",
        timezone_id="Asia/Seoul",
    )

    # 자동화 감지 제거 스크립트
    context.add_init_script(
        """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });

        // Chrome 객체 추가 (자연스러운 브라우저처럼 보이게)
        window.chrome = {
            runtime: {}
        };
    """
    )

    yield context

    # Context 닫을 때 모든 페이지 정리
    try:
        for p in context.pages:
            if not p.is_closed():
                p.close()
    except Exception:
        pass
    context.close()


@pytest.fixture
def page(context):
    """
    각 테스트마다 새로운 페이지를 생성합니다.

    - 기본 타임아웃: 30초
    - 네비게이션 타임아웃: 30초
    """
    try:
        context.clear_cookies()
    except Exception:
        pass

    page = context.new_page()
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(30000)

    yield page

    # 쿠키 삭제
    context.clear_cookies()

    page.close()


# ==================== Logged In Fixtures ====================


@pytest.fixture(scope="session")
def logged_in_context(browser, test_account):
    """
    세션 전체에서 재사용할 수 있는 로그인된 컨텍스트

    한 번만 로그인하고, 이 컨텍스트를 여러 테스트에서 재사용합니다.
    Rate Limiting 문제를 해결합니다.
    """
    from framework.pages.home_page import HomePage

    # 새로운 컨텍스트 생성
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1920, "height": 1080},
        locale="ko-KR",
        timezone_id="Asia/Seoul",
    )

    # 자동화 감지 제거 스크립트
    context.add_init_script(
        """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        window.chrome = { runtime: {} };
        """
    )

    # 임시 페이지를 만들어서 로그인 수행
    temp_page = context.new_page()
    temp_page.set_default_timeout(30000)
    temp_page.set_default_navigation_timeout(30000)

    print("\n🔐 세션용 로그인 수행 중...")
    homepage = HomePage(temp_page)
    homepage.visit()
    homepage.click_login_button(test_account["id"], test_account["password"])
    print("✅ 세션 로그인 완료\n")

    # 로그인에 사용한 임시 페이지는 닫기 (context는 유지!)
    temp_page.close()

    yield context  # 로그인된 context를 반환

    # 모든 테스트 끝난 후에만 context 닫기
    context.close()


@pytest.fixture
def logged_in_page(logged_in_context):
    """
    로그인된 컨텍스트에서 새 페이지를 생성합니다.

    이미 로그인된 상태이므로 다시 로그인할 필요 없습니다.
    로그인이 필요한 테스트에서 사용합니다.
    """
    page = logged_in_context.new_page()
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(30000)

    yield page

    try:
        # context에 열린 모든 페이지 확인
        for p in logged_in_context.pages:
            if not p.is_closed():
                p.close()
                print(f"🧹 페이지 닫음: {p.url if hasattr(p, 'url') else '알 수 없음'}")
    except Exception as e:
        print(f"⚠️ 페이지 정리 중 오류: {e}")


# ==================== Test Account Fixture ====================


@pytest.fixture(scope="session")
def test_account():
    """
    테스트 계정 정보를 제공합니다.

    .env 파일에서 TEST_ID, TEST_PASSWORD를 읽어옵니다.
    환경 변수가 설정되지 않은 경우 테스트를 스킵합니다.

    Returns:
        dict: {'id': str, 'password': str}
    """
    test_id = os.getenv("TEST_ID")
    test_password = os.getenv("TEST_PASSWORD")

    if not test_id or not test_password:
        pytest.skip("테스트 계정 정보가 설정되지 않았습니다. .env 파일을 확인하세요.")

    return {"id": test_id, "password": test_password}


# ==================== Pytest Hooks ====================


def pytest_configure(config):
    """
    pytest 실행 전 필요한 디렉토리를 생성합니다.

    - reports/
    - reports/screenshots/
    - videos/
    """
    os.makedirs("reports", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)


def pytest_html_report_title(report):
    """pytest-html 리포트 제목을 변경합니다."""
    report.title = "G마켓 자동화 테스트 리포트"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    테스트 실패 시 자동으로 스크린샷을 저장합니다.

    - 실패한 테스트의 스크린샷을 reports/screenshots/에 저장
    - pytest-html 리포트에 스크린샷 첨부
    """
    outcome = yield
    rep = outcome.get_result()

    # 테스트 실패 시에만 스크린샷 저장
    if rep.when == "call" and rep.failed:
        if hasattr(item, "funcargs") and "page" in item.funcargs:
            page = item.funcargs["page"]

            try:
                # 페이지가 닫혀있지 않은지 확인
                if not page.is_closed():
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_path = f"reports/screenshots/{item.name}_{timestamp}.png"
                    os.makedirs("reports/screenshots/", exist_ok=True)

                    page.screenshot(path=screenshot_path)
                    print(f"\n📸 스크린샷 저장: {screenshot_path}")

                    # pytest-html 리포트에 스크린샷 첨부
                    if hasattr(rep, "extra"):
                        rep.extra.append(pytest_html.extras.image(screenshot_path))
                else:
                    print("\n⚠️  페이지가 닫혀있어 스크린샷을 저장할 수 없습니다.")

            except Exception as e:
                print(f"\n❌ 스크린샷 저장 실패: {e}")
