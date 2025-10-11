import pytest
from playwright.sync_api import sync_playwright
import os
from datetime import datetime
from dotenv import load_dotenv
import pytest_html

load_dotenv()

# 전체 테스트 세션동안 딱 1번 실행
@pytest.fixture(scope='session')
def browser():
    with sync_playwright() as p:
        headless = os.getenv('HEADLESS', 'false').lower() == 'true'

        # 🤖 봇 탐지 우회를 위한 기본 설정
        browser = p.chromium.launch(
            headless=headless,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
                '--disable-automation',
                '--exclude-switches=enable-automation'
            ]
        )
        yield browser
        browser.close()


# 각 테스트마다 새로운 context 생성
@pytest.fixture
def context(browser):
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport={'width': 1920, 'height': 1080},
        locale='ko-KR',
        timezone_id='Asia/Seoul'
    )

    # 자동화 감지 제거
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });

        // Chrome 객체 추가 (자연스러운 브라우저처럼 보이게)
        window.chrome = {
            runtime: {}
        };
    """)

    yield context
    context.close()


# 각 테스트마다 새로운 page 생성
@pytest.fixture
def page(context):
    page = context.new_page()
    yield page
    page.close()

#HTML 리포트 제목 변경
def pytest_html_report_title(report):
    report.title = "G마켓 자동화 테스트 리포트"

# 테스트 실패시 스크린샷 자동 저장
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # 테스트 실패시 스크린샷 저장
    if rep.when == 'call' and rep.failed:
        if hasattr(item, "funcargs") and "page" in item.funcargs:
            page = item.funcargs["page"]

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"reports/screenshots/{item.name}_{timestamp}.png"
            os.makedirs("reports/screenshots/", exist_ok=True)
            page.screenshot(path=screenshot_path)
            print(f"\n📸 스크린샷 저장: {screenshot_path}")

            if hasattr(rep, 'extra'):
                rep.extra.append(pytest_html.extras.image(screenshot_path))

# 테스트 계정 정보
@pytest.fixture(scope='session')
def test_account():
    test_id = os.getenv('TEST_ID')
    test_password = os.getenv('TEST_PASSWORD')

    if not test_id or not test_password:
        pytest.skip("테스트 계정 정보가 설정되지 않았습니다. .env파일을 확인하세요")
    return { 'id': test_id, 'password': test_password}


# pytest 시작시 폴더 생성
def pytest_configure(config):
    os.makedirs("reports", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)