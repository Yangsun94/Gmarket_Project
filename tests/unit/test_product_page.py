import pytest

from framework.pages.home_page import HomePage
from framework.pages.product_page import ProductPage


class TestProductPageBasic:
    # should_be_on_product_page() 테스트
    @pytest.mark.smoke
    def test_product_page_loads(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("마우스")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        result = product_page.should_be_on_product_page()

        assert result is product_page

    # get_product_info() 테스트
    @pytest.mark.smoke
    @pytest.mark.parametrize("keyword", ["노트북", "이어폰", "스피커"])
    def test_get_product_info_multiple_products(self, page, keyword):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product(keyword)
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

        info = product_page.get_product_info()

        assert info is not None, f"{keyword} 상품 정보를 가져올 수 없습니다"
        assert info["title"], "상품명이 비어있습니다"
        assert info["price"], "가격이 비어있습니다"
        assert info["shipping"], "배송 정보가 비어있습니다"


class TestProductPageScroll:
    # scroll_and_explore() 테스트
    def test_scroll_and_explore(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("모니터")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

        # 스크롤 전 위치 확인
        initial_y = page.evaluate("window.scrollY")

        # 스크롤 실행
        product_page.scroll_and_explore()

        # 스크롤 후 상단 복귀 확인 (0에 가까운지)
        final_y = page.evaluate("window.scrollY")
        assert final_y == initial_y, "페이지 상단으로 돌아오지 않았습니다"

    # scroll_and_explore() 이후 add_to_cart(quantity=1) 테스트
    @pytest.mark.slow
    def test_scroll_then_add_to_cart(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("충전기")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

        # 페이지 탐색
        product_page.scroll_and_explore()

        # 장바구니 담기
        result = product_page.add_to_cart(1)
        assert result is True, "장바구니 담기 실패"


class TestProductPageAddToCart:
    # add_to_cart(quantity) 테스트
    @pytest.mark.cart
    @pytest.mark.parametrize("quantity", [2, 3, 5])
    def test_add_to_cart_multiple_quantities(self, page, quantity):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("마우스")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

        result = product_page.add_to_cart(quantity)

        if result is False:
            pytest.skip("모든 옵션이 품절입니다")

        assert result is True, "옵션 선택 및 담기 실패"


class TestProductPageNavigation:
    #
    @pytest.mark.smoke
    def test_click_logo_returns_homepage(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("헤드셋")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

        returned_homepage = product_page.click_logo()
        returned_homepage.should_be_on_homepage()

        assert isinstance(returned_homepage, HomePage), "로고 클릭 실패"

    # click_cart_button() 테스트
    @pytest.mark.cart
    def test_click_cart_button(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("USB")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()

    #  click_login_button(username,password) 테스트
    @pytest.mark.login
    def test_login_from_product_page(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("게이밍마우스")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

        result = product_page.click_login_button(test_account["id"], test_account["password"])

        assert result is not None, "로그인 실패"
        assert isinstance(result, ProductPage), "ProductPage 객체가 반환되지 않았습니다"

    # logout() 테스트
    @pytest.mark.login
    def test_logout_from_product_page(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("태블릿")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

        product_page.click_login_button(test_account["id"], test_account["password"])

        returned_homepage = product_page.logout()

        assert returned_homepage is not None, "로그아웃 실패"
        assert isinstance(returned_homepage, HomePage), "HomePage 객체가 반환되지 않았습니다"
