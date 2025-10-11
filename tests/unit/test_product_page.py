import pytest

from framework.pages.home_page import HomePage


class TestProductPage:
    # 상품 페이지 정상적으로 로드되는지 테스트
    @pytest.mark.smoke
    def test_product_page_loads_successfully(self, page):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

    # 상품 정보 가져오기
    def test_product_info(self, page):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_info = product_page.get_product_info()

        # 값이 비어있지 않은지 확인
        assert len(product_info["title"]) > 0
        assert len(product_info["price"]) > 0
        assert len(product_info["shipping"]) > 0


class TestProductPageExploration:
    # 페이지 탐색 테스트
    def test_scroll_and_explor(self, page):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.scroll_and_explore()


class TestProductPageCart:
    # 장바구니 담기 테스트
    @pytest.mark.slow
    @pytest.mark.parametrize("quantity", [2, 3, 5])
    def test_add_to_cart(self, page, quantity):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

        product_page.add_to_cart(quantity)


class TestProductPageNavigation:
    # 로고 클릭 테스트
    def test_return_to_home_via_logo(self, page):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.click_logo()

    # 로그인 테스트
    @pytest.mark.login
    def test_login_from_product_page(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

        product_page.click_login_button(test_account["id"], test_account["password"])

    # 로그아웃 테스트
    @pytest.mark.login
    def test_logout_from_product_page(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

        product_page.click_login_button(test_account["id"], test_account["password"])

        homepage = product_page.logout()
        homepage.should_be_on_homepage()

    # 장바구니 테스트
    def test_cart_from_product_page(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()
