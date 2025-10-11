import pytest

from framework.pages.home_page import HomePage


class TestCartPageBasic:
    # 장바구니 페이지가 정상적으로 로드되는지 확인
    @pytest.mark.smoke
    def test_cart_page_loads_successfully(self, page):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()

    # 빈 장바구니 상태 확인
    def test_empty_cart(self, page):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()
        cart_page.clear_cart()

        items = cart_page.get_cart_items()
        assert len(items) == 0, "장바구니가 비어있어야 합니다"


class TestCartPageItems:
    # 장바구니 상품 목록 가져오기
    @pytest.mark.slow
    def test_get_cart_items(self, page):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart()

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()

        # 상품 목록 확인
        items = cart_page.get_cart_items()
        assert len(items) > 0, "장바구니에 상품이 있어야 합니다"


class TestCartPageQuantity:
    # 수량 증가 테스트
    @pytest.mark.slow
    def test_increase_quantity(self, page):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart()

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()
        cart_page.update_quantity(index=1, quantity=3)

    # 수량 감소 테스트
    @pytest.mark.slow
    def test_decrease_quantity(self, page):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(5)

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()
        cart_page.update_quantity(index=1, quantity=4)

    """
class TestCartPageRemove:
    """

    # 단일 상품 삭제 테스트
    @pytest.mark.slow
    def test_remove_single_item(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()
        homepage.click_login_button(test_account["id"], test_account["password"])

        # 첫 번째 상품 담기
        search_page = homepage.search_product("마우스")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(2)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(2)

        # 두 번째 상품 담기
        homepage = product_page.click_logo()
        search_page = homepage.search_product("키보드")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(2)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(3)

        # 장바구니 확인
        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()

        cart_page.remove_item(1)


class TestCartPagePrice:
    # 총 금액 추출 테스트
    @pytest.mark.slow
    def test_get_total_price(self, page):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("충전 케이블")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(2)

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()

        total_price = cart_page.get_total_price()
        assert total_price is not None


class TestCartPageNavigation:
    # 로고 클릭 테스트
    def test_return_to_home_via_logo(self, page):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()

        # 로고 클릭
        homepage = cart_page.click_logo()
        homepage.should_be_on_homepage()

    # 결제 페이지 이동 테스트
    @pytest.mark.slow
    def test_cart_to_checkout_navigation(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()
        homepage.click_login_button(test_account["id"], test_account["password"])

        search_page = homepage.search_product("자물쇠")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(2)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(3)

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()

        cart_page.proceed_to_checkout()
