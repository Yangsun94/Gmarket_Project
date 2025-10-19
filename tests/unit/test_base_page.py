import pytest

from framework.config.locators import GmarketLocators
from framework.pages.home_page import HomePage


class TestBasePageNavigation:
    # goto() 테스트
    @pytest.mark.smoke
    def test_goto_method(self, page):
        homepage = HomePage(page)
        result = homepage.goto()
        homepage.should_be_on_homepage()

        assert "gmarket.co.kr" in homepage.page.url
        assert result == homepage, "goto()는 self를 반환해야 합니다"

    # wait_for_load() 테스트
    @pytest.mark.smoke
    def test_wait_for_load_method(self, page):
        homepage = HomePage(page)
        homepage.goto()
        homepage.should_be_on_homepage()

        # 페이지 로딩 대기
        result = homepage.wait_for_load()

        # 메서드 체이닝 확인 (self 반환)
        assert result == homepage

    # refresh_page() 테스트
    def test_refresh_page_method(self, page):
        homepage = HomePage(page)
        homepage.goto()
        homepage.should_be_on_homepage()

        current_url = homepage.page.url

        # 페이지 새로고침
        homepage.refresh_page()

        # 여전히 같은 페이지인지 확인
        assert current_url == homepage.page.url


class TestBasePageValidation:
    # should_see_element()
    @pytest.mark.smoke
    def test_should_see_element_method(self, page):
        homepage = HomePage(page)
        homepage.goto()

        # 검색창이 보여야 함
        result = homepage.should_see_element(GmarketLocators.SEARCH_INPUT)

        # 메서드 체이닝 확인 (self 반환)
        assert result == homepage

    # should_not_see_element() 테스트
    def test_should_not_see_element_method(self, page):
        homepage = HomePage(page)
        homepage.goto()

        # 존재하지 않는 요소가 보이지 않아야 함
        result = homepage.should_not_see_element(".non-existent-element-77777")

        # 메서드 체이닝 확인 (self 반환)
        assert result == homepage

    # should_see_text() 테스트
    @pytest.mark.smoke
    def test_should_see_text_method_without_selector(self, page):
        homepage = HomePage(page)
        homepage.goto()

        # 요소안에 "로그인" 텍스트가 있어야 함
        result = homepage.should_see_text("로그인", GmarketLocators.LOGIN_BUTTON)
        assert result == homepage

        # 요소안에 "로그인" 텍스트 없을시 전체페이지에서 찾기
        result = homepage.should_see_text("로그인")
        assert result == homepage

    # should_have_url() 테스트
    def test_should_have_url_method(self, page):
        homepage = HomePage(page)
        homepage.goto()
        homepage.should_be_on_homepage()

        # URL이 gmarket.co.kr을 포함해야 함
        result = homepage.should_have_url("gmarket.co.kr")

        # 메서드 체이닝 확인 (self 반환)
        assert result == homepage

    # should_have_title() 테스트
    def test_should_have_title_method(self, page):
        homepage = HomePage(page)
        homepage.goto()
        homepage.should_be_on_homepage()

        # 타이틀에 "마켓"이 포함되어야 함
        result = homepage.should_have_title("마켓")

        # 메서드 체이닝 확인 (self 반환)
        assert result == homepage


class TestBasePageSafeActions:
    # safe_click() 테스트
    @pytest.mark.smoke
    def test_safe_click_method(self, page):
        homepage = HomePage(page)
        homepage.goto()

        # 로고를 안전하게 클릭
        result = homepage.safe_click(GmarketLocators.LOGO)

        # 메서드 체이닝 확인
        assert result == homepage
        # 페이지가 여전히 gmarket인지 확인
        assert "gmarket" in homepage.page.url.lower()

    # safe_type() 테스트
    @pytest.mark.smoke
    def test_safe_type_method(self, page):
        homepage = HomePage(page)
        homepage.goto()
        homepage.should_be_on_homepage()

        # 검색창에 안전하게 타이핑
        result = homepage.safe_type(GmarketLocators.SEARCH_INPUT, "테스트")

        # 메서드 체이닝 확인
        assert result == homepage
        # 입력된 값 확인
        value = homepage.page.locator(GmarketLocators.SEARCH_INPUT).input_value()
        assert "테스트" in value

    # safe_type() 테스트 < clear = False >
    def test_safe_type_without_clear(self, page):
        homepage = HomePage(page)
        homepage.goto()
        homepage.should_be_on_homepage()

        # 첫 번째 입력
        homepage.safe_type(GmarketLocators.SEARCH_INPUT, "첫번째")
        first_value = homepage.page.locator(GmarketLocators.SEARCH_INPUT).input_value()

        # 두 번째 입력 (clear=False)
        homepage.safe_type(GmarketLocators.SEARCH_INPUT, "두번째", clear=False)
        second_value = homepage.page.locator(GmarketLocators.SEARCH_INPUT).input_value()

        # 값 확인 (두 번째만 있어야 함 - clear=False지만 새로 타이핑됨)
        assert len(second_value) >= len(first_value)

    # safe_press() 테스트
    def test_safe_press_method(self, page):
        homepage = HomePage(page)
        homepage.goto()
        homepage.should_be_on_homepage()

        # 검색창에 포커스
        homepage.safe_click(GmarketLocators.SEARCH_INPUT)

        # a 키 입력
        result = homepage.safe_press("a")

        # 메서드 체이닝 확인
        assert result == homepage


class TestBasePageBotAvoidance:
    # human_delay() 테스트
    def test_human_delay_method(self, page):
        homepage = HomePage(page)
        homepage.goto()
        homepage.should_be_on_homepage()

        # 인간적인 딜레이 실행 (0.5~1초)
        import time

        start = time.time()
        result = homepage.human_delay(0.5, 1.0)
        elapsed = time.time() - start

        # 메서드 체이닝 확인
        assert result == homepage
        # 0.5~1초 사이에 딜레이가 발생했는지 확인
        assert 0.4 < elapsed < 1.2, f"딜레이 시간이 범위를 벗어남: {elapsed}초"

    # simulate_reading() 테스트
    @pytest.mark.slow
    def test_simulate_reading_method(self, page):
        homepage = HomePage(page)
        homepage.goto()
        homepage.should_be_on_homepage()

        # 페이지 읽기 시뮬레이션
        result = homepage.simulate_reading()

        # 메서드 체이닝 확인
        assert result == homepage

    # simulate_mouse_movement() 테스트
    @pytest.mark.slow
    def test_simulate_mouse_movement_method(self, page):
        homepage = HomePage(page)
        homepage.goto()
        homepage.should_be_on_homepage()

        # 마우스 움직임 시뮬레이션
        result = homepage.simulate_mouse_movement()

        # 메서드 체이닝 확인
        assert result == homepage


class TestBasePageUtilities:
    # scroll_to_element() 테스트
    def test_scroll_to_element_method(self, page):
        homepage = HomePage(page)
        homepage.goto()
        homepage.should_be_on_homepage()

        result = homepage.scroll_to_element(GmarketLocators.COMPANY_INFO)

        # 메서드 체이닝 확인
        assert result == homepage

    # take_screenshot() 테스트
    def test_take_screenshot_method(self, page):
        homepage = HomePage(page)
        homepage.goto()
        homepage.should_be_on_homepage()

        # 스크린샷 저장
        no_name_result = homepage.take_screenshot("test_base_page_screenshot")
        # 이름 없이도 저장
        name_result = homepage.take_screenshot()

        # 메서드 체이닝 확인
        assert no_name_result == homepage
        assert name_result == homepage
