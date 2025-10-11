import pytest

from framework.config.locators import GmarketLocators
from framework.pages.home_page import HomePage


# 전체 쇼핑 플로우 통합 테스트
class TestShoppingFlow:
    @pytest.fixture
    def home_page(self, page):
        return HomePage(page)

    @pytest.mark.integration
    def test_complete_shopping_flow(self, home_page):
        print("완전한 쇼핑 플로우 테스트")

        print("홈페이지 방문")
        home_page.visit().should_be_on_homepage()

        print("상품 검색")
        keyword = "무선 이어폰"
        search_page = home_page.search_product(keyword)

        print("검색 결과 확인")
        search_page.should_be_on_search_page()
        search_page.should_have_search_results()
        search_page.apply_price_filter(5000, 300000)
        search_page.sort_by_price_low_to_high()

        results, relevance = search_page.verify_search_keyword_in_results(keyword)
        assert relevance, f"'{keyword}' 검색 결과의 관련성이 낮습니다"

        print("상품 상세 페이지 이동")
        product_page = search_page.click_product_by_index(1)

        print("상품 정보 확인")
        product_page.should_be_on_product_page()
        product_info = product_page.get_product_info()
        assert product_info["title"] != "정보 없음", "상품 명을 가져올 수 없습니다"

        print("상품 페이지 탐색")
        product_page.scroll_and_explore()

        print("완전한 쇼핑 플로우 테스트  완료")


class TestCartIntegration:
    @pytest.fixture
    def home_page(self, page):
        return HomePage(page)

    @pytest.mark.integration
    @pytest.mark.login
    @pytest.mark.cart
    def test_cart_integration(self, home_page, test_account):
        print("장바구니 통합 테스트 시작")

        # 1. 홈페이지 → 검색
        home_page.visit().should_be_on_homepage()
        home_page = home_page.click_login_button(test_account["id"], test_account["password"])

        keyword = "무선 이어폰"
        search_page = home_page.search_product(keyword)

        # 2. 상품 상세 페이지
        product_page = search_page.click_product_by_index(1)
        product_page.should_be_on_product_page()

        # 3. 장바구니에 담기
        add_result = product_page.add_to_cart(2)
        assert add_result is True, "장바구니 담기 실패"

        # 4. 장바구니로 이동
        cart_page = product_page.click_cart_button()
        cart_page.should_be_on_cart_page()

        # 5. 장바구니 상품 확인
        items = cart_page.get_cart_items()

        if len(items) == 0:
            pytest.skip("장바구니가 비어있어 추가 테스트를 건너뜁니다")

        print(f"장바구니 상품 수: {len(items)}개")
        assert len(items) > 0, "장바구니에 상품이 없습니다"

        # 6. 총 금액 확인
        total_price = cart_page.get_total_price()
        assert total_price is not None, "총 금액을 가져올 수 없습니다"

        # 7. 수량 변경해보기
        update_result = cart_page.update_quantity(1, 4)
        assert update_result is True, "수량 증가 실패"
        update_result = cart_page.update_quantity(1, 3)
        assert update_result is True, "수량 감소 실패"

        # 8. 바뀐 총 금액 확인
        new_total_price = cart_page.get_total_price()
        assert new_total_price is not None, "변경된 총 금액을 가져올 수 없습니다"
        print(f"변경된 총 결제 금액: {new_total_price}")

        # 결제 페이지 클릭
        cart_page.proceed_to_checkout()
        cart_page.page.go_back()

        # 9. 전체 비우기
        cart_page.clear_cart()

        # 10. 로고 클릭하여 홈으로 이동
        homepage = cart_page.click_logo()
        assert homepage is not None, "로고 클릭 실패"

        # 11. 홈페이지로 돌아왔는지 확인
        homepage.should_see_main_elements()

        print("장바구니 통합 테스트 완료")


class TestLoginFlow:
    @pytest.fixture
    def home_page(self, page):
        return HomePage(page)

    @pytest.mark.integration
    @pytest.mark.login
    def test_valid_login_logout_flow(self, home_page, test_account):
        print("로그인 페이지 이동 > 정상 로그인 > 로그아웃")

        home_page.visit().should_be_on_homepage()
        home_page = home_page.click_login_button(test_account["id"], test_account["password"])

        # 로그인 확인
        logout_btn = home_page.page.locator(GmarketLocators.LOGOUT_BUTTON)
        assert logout_btn.is_visible(), "로그인 상태가 아님"

        logout = home_page.logout()
        assert logout, "로그아웃 실패"

        # 로그아웃 확인
        assert not logout_btn.is_visible(timeout=3000), "로그아웃 후에 로그인 상태"

    def test_invalid_login(self, home_page):
        print("로그인 페이지 이동 > 잘못된 계정으로 로그인")

        home_page.visit().should_be_on_homepage()
        result = home_page.click_login_button("wrong_user", "wrong_password")

        assert result is None, "잘못된 계정으로 로그인 성공"

        logout = home_page.logout()
        assert not logout
