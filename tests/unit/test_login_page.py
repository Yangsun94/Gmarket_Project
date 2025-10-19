import pytest

from framework.config.locators import LoginPageLocators
from framework.pages.home_page import HomePage
from framework.pages.login_page import LoginPage


class TestLogin:
    # 정상 계정으로 로그인
    @pytest.mark.login
    @pytest.mark.smoke
    def test_login_with_valid_credentials(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        homepage.page.click('a:has-text("로그인")')
        homepage.wait_for_load()

        login_page = LoginPage(page)
        login_page.should_be_on_login_page()
        result = login_page.login(test_account["id"], test_account["password"])

        assert result, "로그인에 실패하였습니다"

    # 잘못된 계정으로 로그인
    @pytest.mark.login
    def test_login_with_invalid_credentials(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        homepage.page.click('a:has-text("로그인")')
        homepage.wait_for_load()

        login_page = LoginPage(page)
        login_page.should_be_on_login_page()
        result = login_page.login("wrong_user", "wrong_pass")

        assert not result, "로그인에 성공해서는 안됩니다"

    # 빈 계정으로 로그인시도
    @pytest.mark.login
    def test_login_with_empty_credentials(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        homepage.page.click('a:has-text("로그인")')
        homepage.wait_for_load()

        login_page = LoginPage(page)
        login_page.should_be_on_login_page()
        result = login_page.login("", "")

        assert not result or result is None, "빈 계정으로 로그인 성공해서는 안됩니다"

    @pytest.mark.login
    @pytest.mark.smoke
    def test_successful_login(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        assert homepage.is_login_button_visible(), "로그인 버튼이 보여야 함"

        result = homepage.click_login_button(test_account["id"], test_account["password"])

        assert result is not None, "로그인이 실패했습니다"
        assert not homepage.is_login_button_visible(), "로그인 후 로그인 버튼이 사라져야 함"


class TestIsLoggedInMethod:
    # is_logged_in() 상태 변화 테스트 (로그인 전 > 로그인 후 > 로그아웃 후)
    @pytest.mark.login
    @pytest.mark.smoke
    def test_login_method_directly(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        # LoginPage 인스턴스 생성
        login_page = LoginPage(page)

        # 로그인 전
        assert not login_page.is_logged_in(), "로그인 전에는 False여야 함"

        homepage.click_login_button(test_account["id"], test_account["password"])

        # 로그인 후
        assert login_page.is_logged_in(), "로그인 후에는 True여야 함"

        homepage.logout()

        # 로그아웃 후
        assert not login_page.is_logged_in(), "로그아웃 후에는 False여야 함"

    # 페이지 이동 후에도 로그인 상태 유지 확인
    @pytest.mark.login
    def test_is_logged_in_status_persistence_across_pages(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit()
        homepage.should_be_on_homepage()

        login_page = LoginPage(logged_in_page)
        assert login_page.is_logged_in(), "로그인 직후: True"

        # 검색 페이지로 이동
        search_page = homepage.search_product("마우스")
        search_page.should_be_on_search_page()

        # 여전히 로그인 상태인지 확인
        assert login_page.is_logged_in(), "페이지 이동 후에도 로그인 상태 유지"

        # 홈으로 다시 이동
        search_page.click_logo()

        # 여전히 로그인 상태인지 확인
        assert login_page.is_logged_in(), "홈으로 돌아온 후에도 로그인 상태 유지"


class TestLoginPageNavigation:
    # 홈페이지에서 로그인 페이지로 이동
    @pytest.mark.login
    def test_navigate_to_login_page_from_homepage(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        # 로그인 버튼 클릭
        homepage.page.click('a:has-text("로그인")')
        homepage.wait_for_load()

        # 로그인 페이지 확인
        login_page = LoginPage(page)
        assert login_page.should_be_on_login_page() is not None, "로그인페이지로 진입 안됨"

    # 검색페이지에서 로그인 페이지로 이동
    @pytest.mark.login
    def test_navigate_to_login_page_from_searchpage(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("마우스")
        search_page.should_be_on_search_page()

        search_page.page.click('a:has-text("로그인")')
        search_page.wait_for_load()

        # 로그인 페이지 확인
        login_page = LoginPage(page)
        assert login_page.should_be_on_login_page() is not None, "로그인페이지로 진입 안됨"

    # 상품 페이지(새 탭)에서 로그인 페이지로 이동
    @pytest.mark.login
    def test_navigate_to_login_page_from_productpage(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("마우스")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

        product_page.page.click('a:has-text("로그인")')
        product_page.wait_for_load()

        # 로그인 페이지 확인
        login_page = LoginPage(product_page.page)
        assert login_page.should_be_on_login_page() is not None, "로그인페이지로 진입 안됨"

    # 장바구니 페이지에서 로그인 페이지로 이동
    @pytest.mark.login
    def test_navigate_to_login_page_from_cartpage(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()

        cart_page.page.click('a:has-text("로그인")')
        cart_page.wait_for_load()

        # 로그인 페이지 확인
        login_page = LoginPage(page)
        assert login_page.should_be_on_login_page() is not None, "로그인페이지로 진입 안됨"

    # 로그인 페이지의 필수 요소들이 보이는지 테스트
    @pytest.mark.login
    def test_login_page_elements_visible(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        # 로그인 페이지로 이동
        homepage.page.click('a:has-text("로그인")')
        homepage.wait_for_load()

        login_page = LoginPage(page)
        login_page.should_be_on_login_page()

        # ID 입력창 확인
        assert login_page.page.locator(LoginPageLocators.ID_INPUT).is_visible(), "ID 입력창이 보여야 함"

        # 비밀번호 입력창 확인
        assert login_page.page.locator(LoginPageLocators.PASSWORD_INPUT).is_visible(), "비밀번호 입력창이 보여야 함"

        # 로그인 버튼 확인
        assert login_page.page.locator(LoginPageLocators.LOGIN_BUTTON).is_visible(), "로그인 버튼이 보여야 함"
