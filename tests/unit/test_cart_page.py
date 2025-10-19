import pytest

from framework.pages.cart_page import CartPage
from framework.pages.home_page import HomePage


class TestCartPageBasic:
    # should_be_on_cart_page() 테스트
    @pytest.mark.smoke
    def test_cart_page_loads_successfully(self, page):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()

        assert "cart" in page.url.lower(), "장바구니 페이지가 아닙니다"

    # 빈 장바구니 상태 확인 get_cart_items() 테스트
    def test_empty_cart(self, page):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()
        cart_page.clear_cart()

        items = cart_page.get_cart_items()
        assert len(items) == 0, "장바구니가 비어있어야 합니다"


class TestCartPageItems:
    # get_cart_items() 테스트
    @pytest.mark.slow
    def test_get_cart_items(self, logged_in_page):
        homepage = HomePage(logged_in_page)
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
        cart_item = items[0]

        assert cart_item["title"] != "", "상품명이 비어있습니다"
        assert cart_item["price"] != "", "가격이 비어있습니다"
        assert cart_item["index"] > 0, "인덱스가 유효하지 않습니다"

    # get_cart_items() 테스트
    @pytest.mark.slow
    def test_cart_items_count_accuracy(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit()
        homepage.should_be_on_homepage()

        # 장바구니 비우기
        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()
        cart_page.clear_cart()

        # 상품 2개 추가
        homepage = cart_page.click_logo()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("마우스")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(1)

        homepage = product_page.click_logo()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("키보드")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(1)

        # 장바구니 확인
        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()
        items = cart_page.get_cart_items()

        assert len(items) == 2, f"2개 상품이 있어야 하는데 {len(items)}개입니다"


class TestCartPageQuantity:
    # update_quantity(index, quantity) 테스트(수량증가)
    @pytest.mark.slow
    def test_increase_quantity(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart()

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()
        result = cart_page.update_quantity(index=1, quantity=3)

        assert result is True, "수량 증가 실패"

    # update_quantity(index, quantity) 테스트(수량감소)
    @pytest.mark.slow
    def test_decrease_quantity(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(5)

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()
        result = cart_page.update_quantity(index=1, quantity=4)

        assert result is True, "수량 감소 실패"

    # update_quantity(index, quantity) 테스트(동일수량)
    @pytest.mark.slow
    def test_quantity_no_change(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit().should_be_on_homepage()

        # 상품 3개 추가
        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(3)

        # 동일 수량으로 설정
        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()

        result = cart_page.update_quantity(1, 3)

        assert result is True

    # update_quantity(index, quantity) 테스트(quantity = 0)
    @pytest.mark.slow
    def test_zero_quantity_handling(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit().should_be_on_homepage()

        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()
        cart_page.clear_cart()

        homepage = cart_page.click_logo()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("마우스")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(3)

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()

        # 수량 0으로 설정
        result = cart_page.update_quantity(1, 0)
        assert result

    # update_quantity(index, quantity) 테스트(index = 0)
    @pytest.mark.slow
    def test_zero_index_handling(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit().should_be_on_homepage()

        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()
        cart_page.clear_cart()

        homepage = cart_page.click_logo()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("마우스")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(3)

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()

        # 인덱스 0으로 설정
        result = cart_page.update_quantity(0, 3)
        assert not result

    # update_quantity(index, quantity) 테스트(index > len(items))
    @pytest.mark.slow
    def test_over_index_handling(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit().should_be_on_homepage()

        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()
        cart_page.clear_cart()

        homepage = cart_page.click_logo()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("마우스")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(3)

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()

        # 인덱스 상품개수보다 많게 설정
        result = cart_page.update_quantity(100, 3)
        assert not result


class TestCartPageRemove:
    # remove_item(index) 테스트
    @pytest.mark.slow
    def test_remove_single_item(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit().should_be_on_homepage()

        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()
        cart_page.clear_cart()

        homepage = cart_page.click_logo()
        homepage.should_be_on_homepage()

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

        items_before = cart_page.get_cart_items()
        assert len(items_before) == 2, "장바구니에 2개 상품이 있어야 합니다"

        result = cart_page.remove_item(1)
        assert result is True, "상품 삭제 실패"

        items_after = cart_page.get_cart_items()
        assert len(items_after) == 1, "장바구니에 1개 상품이 남아있어야 합니다"

    # remove_item(index) 테스트(2)
    @pytest.mark.slow
    def test_remove_last_item(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit().should_be_on_homepage()

        # 장바구니 비우기
        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()
        cart_page.clear_cart()

        homepage = cart_page.click_logo()
        homepage.should_be_on_homepage()
        # 상품 3개 추가
        for keyword in ["스피커", "웹캠", "마이크"]:
            search_page = homepage.search_product(keyword)
            search_page.should_be_on_search_page()

            product_page = search_page.click_product_by_index(1)
            product_page.should_be_on_product_page()
            product_page.add_to_cart(1)
            homepage = product_page.click_logo()

        # 장바구니 확인
        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()

        items_before = cart_page.get_cart_items()
        count = len(items_before)
        assert count == 3, "3개 상품이 있어야 합니다"

        # 마지막 삭제
        cart_page.remove_item(count)

        items_after = cart_page.get_cart_items()
        assert len(items_after) == 2, "2개 상품이 남아야 합니다"

    # remove_item(index) 테스트(3)
    @pytest.mark.slow
    def test_remove_all_items_one_by_one(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit().should_be_on_homepage()

        # 장바구니 비우기
        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()
        cart_page.clear_cart()

        homepage = cart_page.click_logo()
        homepage.should_be_on_homepage()

        # 상품 3개 추가
        for keyword in ["램", "SSD", "그래픽카드"]:
            search_page = homepage.search_product(keyword)
            search_page.should_be_on_search_page()

            product_page = search_page.click_product_by_index(1)
            product_page.should_be_on_product_page()
            product_page.add_to_cart(1)

            homepage = product_page.click_logo()
            homepage.should_be_on_homepage()

        # 장바구니 확인
        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()

        items = cart_page.get_cart_items()
        count = len(items)
        assert count == 3, "3개 상품이 있어야 합니다"

        # 하나씩 삭제
        for i in range(count):
            cart_page.remove_item(1)
            items = cart_page.get_cart_items()
            result = count - (i + 1)
            assert len(items) == result, f"{result}개 남아야 하는데 {len(items)}개입니다"

        # 최종 확인
        final_items = cart_page.get_cart_items()
        assert len(final_items) == 0, "장바구니가 비어있어야 합니다"

    # remove_item(index) 테스트(없는 인덱스)
    @pytest.mark.slow
    def test_invalid_index_remove(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit().should_be_on_homepage()

        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()
        cart_page.clear_cart()
        homepage = cart_page.click_logo()

        # 상품 1개만 추가
        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(1)

        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()

        items = cart_page.get_cart_items()
        assert len(items) == 1, "1개 상품이 있어야 합니다"

        # 존재하지 않는 인덱스로 삭제 시도
        result = cart_page.remove_item(99)

        # False 반환 또는 예외 발생 (구현에 따라)
        assert result is False or result is None, "존재하지 않는 인덱스 삭제는 실패해야 합니다"


class TestCartPagePrice:
    # get_total_price() 테스트(빈 장바구니)
    def test_empty_cart_operations(self, page):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        # 장바구니 비우기
        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()
        cart_page.clear_cart()

        items = cart_page.get_cart_items()
        assert len(items) == 0, "장바구니가 비어있어야 합니다"

        total = cart_page.get_total_price()
        # None이거나 0일 수 있음
        assert total is None, "빈 장바구니는 금액이 None이어야 합니다"

    # get_total_price() 테스트
    @pytest.mark.slow
    def test_get_total_price(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("마우스")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(2)

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()

        total_price = cart_page.get_total_price()

        assert total_price is not None, "총 금액을 가져오지 못했습니다"
        assert total_price > 0, "총 금액이 0원보다 커야 합니다"

    # get_total_price() 테스트(수량변경)
    @pytest.mark.slow
    def test_price_update_after_quantity_change(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit().should_be_on_homepage()

        # 상품 1개 추가
        search_page = homepage.search_product("충전기")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(1)

        # 초기 총 금액
        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()

        initial_price = cart_page.get_total_price()
        assert initial_price > 0, "초기 금액이 0보다 커야 합니다"

        # 수량 증가 (1→3)
        cart_page.update_quantity(1, 3)
        increased_price = cart_page.get_total_price()

        assert increased_price > initial_price, "수량 증가 후 금액이 증가해야 합니다"

        # 수량 감소 (3→2)
        cart_page.update_quantity(1, 2)
        decreased_price = cart_page.get_total_price()

        assert decreased_price < increased_price, "수량 감소 후 금액이 감소해야 합니다"
        assert decreased_price > initial_price, "2개는 1개보다 비싸야 합니다"

    # get_total_price() 테스트(여러상품)
    @pytest.mark.slow
    def test_multiple_items_total(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit().should_be_on_homepage()

        # 장바구니 비우기
        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()
        cart_page.clear_cart()

        # 상품 2개 추가
        homepage = cart_page.click_logo()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("마우스")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(1)

        homepage = product_page.click_logo()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("키보드")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(1)

        # 총 금액 확인
        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()

        total_price = cart_page.get_total_price()
        assert total_price > 0, "총 금액이 0보다 커야 합니다"


class TestCartPageNavigation:
    # click_logo() 테스트
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
    def test_cart_to_checkout_navigation(self, page, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("자물쇠")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(2)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(3)

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()

        cart_page.proceed_to_checkout()

        assert "checkout" in cart_page.page.url, "결제 페이지로 이동하지 못했습니다"

    # 장바구니에서 뒤로가기 테스트
    def test_back_button_from_cart(self, page):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        # 검색 후 장바구니 이동
        search_page = homepage.search_product("태블릿")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()

        # 뒤로가기
        cart_page.page.go_back()
        cart_page.wait_for_load()

        assert "item" in cart_page.page.url.lower(), "상품 페이지로 돌아가지 못했습니다"

    # 새로고침 후 장바구니 상태 보기
    @pytest.mark.slow
    def test_cart_state_after_refresh(self, logged_in_page):
        homepage = HomePage(logged_in_page)
        homepage.visit().should_be_on_homepage()

        # 상품 추가
        search_page = homepage.search_product("선풍기")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()
        product_page.add_to_cart(2)

        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()

        items_before = cart_page.get_cart_items()
        count_before = len(items_before)

        # 새로고침
        cart_page.page.reload()
        cart_page.should_be_on_cart_page()

        # 상태 확인
        items_after = cart_page.get_cart_items()
        count_after = len(items_after)

        assert count_after == count_before


class TestCartPageLogin:
    #  click_login_button(username,password) 테스트
    @pytest.mark.login
    def test_login_from_cart_page(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()

        result = cart_page.click_login_button(test_account["id"], test_account["password"])

        assert result is not None, "로그인 실패"
        assert isinstance(result, CartPage), "CartPage 객체가 반환되지 않았습니다"

    # logout() 테스트
    @pytest.mark.login
    def test_logout_from_cart_page(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        cart_page = homepage.click_cart_button()
        cart_page.should_be_on_cart_page()

        cart_page.click_login_button(test_account["id"], test_account["password"])

        returned_homepage = cart_page.logout()

        assert returned_homepage is not None, "로그아웃 실패"
        assert isinstance(returned_homepage, HomePage), "HomePage 객체가 반환되지 않았습니다"
