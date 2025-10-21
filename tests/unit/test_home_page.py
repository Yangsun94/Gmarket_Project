import pytest

from framework.pages.home_page import HomePage


class TestHomePage:
    # visit(), should_be_on_homepage() 테스트
    @pytest.mark.smoke
    def test_homepage_loads_successfully(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

    # should_see_main_elements() 테스트
    @pytest.mark.smoke
    def test_main_elements_visible(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        homepage.should_see_main_elements()

    # wait_for_page_load() 테스트
    def test_wait_for_page_load(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        result = homepage.wait_for_page_load()

        assert result == homepage
        homepage.should_be_on_homepage()


class TestHomePageSearch:
    # 클릭으로 검색 테스트
    @pytest.mark.smoke
    @pytest.mark.parametrize("keyword", ["마우스", "노트북", "뭭뤡"])
    def test_search_with_button(self, page, keyword):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product(keyword)
        search_page.should_be_on_search_page()

    # Enter키로 검색 테스트
    @pytest.mark.parametrize("keyword", ["갤럭시", "태블릿", "줵숄"])
    def test_search_with_enter(self, page, keyword):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_with_enter(keyword)
        search_page.should_be_on_search_page()

    # 자동완성 표시 테스트
    @pytest.mark.slow
    def test_search_suggestions_appear(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()
        homepage.type_in_search_without_submit("아이폰")
        suggestions = homepage.should_see_search_suggestions()

        assert suggestions.count() > 0, "자동완성 목록이 비어있습니다"


class TestHomePageNavigation:
    # 로고 클릭시 핫추픽 사이트로 이동 테스트
    @pytest.mark.smoke
    def test_click_logo_stays_on_homepage(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()
        homepage.click_logo()

    # 장바구니 이동 테스트
    def test_cart_button_navigation(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()

    # 로그인 테스트
    @pytest.mark.login
    def test_login_button_navigation(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        result = homepage.click_login_button(test_account["id"], test_account["password"])
        assert result is not None, "로그인 실패"
        assert isinstance(result, HomePage), "HomePage 객체가 반환되지 않았습니다"

    # click_login_button(username,password) 테스트(잘못된 계정으로 로그인)
    @pytest.mark.login
    def test_invalid_login_homepage(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        result = homepage.click_login_button("wrong_id", "wrong_password")

        assert not result, "로그인에 성공해서는 안됩니다"

    #  click_login_button(username,password) 테스트(로그인 상태)
    @pytest.mark.login
    def test_login_from_login_homepage(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        homepage.click_login_button(test_account["id"], test_account["password"])

        result = homepage.click_login_button(test_account["id"], test_account["password"])

        assert result is None, "로그인 실패"

    # 로그아웃 테스트
    @pytest.mark.login
    def test_logout_functionality(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        homepage.click_login_button(test_account["id"], test_account["password"])

        homepage = homepage.logout()
        assert homepage is not None, "로그아웃 실패로 homepage가 None입니다"
        assert homepage.is_login_button_visible(), "로그인 버튼이 표시되지 않습니다"

    # logout() 테스트(로그아웃 상태에서)
    @pytest.mark.login
    def test_logout_from_logout_homepage(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        returned_homepage = homepage.logout()

        assert not returned_homepage, "로그아웃 성공"


class TestHomePageUserBehavior:
    # 카테고리에 마우스 hover 테스트
    def test_hover_over_categories(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()
        homepage.hover_over_categories()


class TestHomePageBehavior:
    # 자연스러운 둘러보기 테스트
    @pytest.mark.slow
    def test_natural_browsing(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()
        homepage.browse_homepage_naturally()


class TestHomePageErrors:
    # 페이지 로드시 에러메세지 없는지 테스트
    def test_no_error_messages_on_load(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()
        homepage.verify_no_errors()


class TestSearchPageEdgeCases:
    # 특수문자, 영문, 숫자 검색 테스트
    @pytest.mark.slow
    @pytest.mark.parametrize("keyword", ["USB-C 케이블", "아이폰 15", "Iphone", "갤럭시 Galaxy"])
    def test_search_with_special_characters(self, page, keyword):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product(keyword)
        search_page.should_be_on_search_page()
