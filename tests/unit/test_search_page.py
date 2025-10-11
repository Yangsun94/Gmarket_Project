import pytest

from framework.pages.home_page import HomePage


class TestSearchPage:
    # 검색 페이지가 정상적으로 로드되는지 확인
    @pytest.mark.smoke
    def test_search_page_loads_successfully(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("마우스")
        search_page.should_be_on_search_page()

    # 검색 결과가 존재하는지 확인
    @pytest.mark.smoke
    @pytest.mark.parametrize("keyword,min_results", [("마우스", 1), ("키보드", 10000)])
    def test_search_results_exist(self, page, keyword, min_results):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product(keyword)
        search_page.should_be_on_search_page()
        search_page.should_have_search_results(min_results)

    # 검색 결과가 검색어와 관련 있는지 테스트
    @pytest.mark.parametrize("keyword", ["마우스", "아이폰", "갤럭시"])
    def test_search_keyword_relevance(self, page, keyword):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product(keyword)
        search_page.should_be_on_search_page()
        search_page.verify_search_keyword_in_results(keyword)

    # 여러 상품 제목 리스트 가져오기 테스트
    def test_get_all_product(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("키보드")
        titles = search_page.get_all_product_titles()

        assert len(titles) > 0, "상품 제목을 가져오지 못했습니다"

    # 여러 상품을 클릭 테스트
    @pytest.mark.parametrize("index", [1, 2, 3])
    def test_click_multiple_products(self, page, index):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(index)
        product_page.should_be_on_product_page()

    # 가격 범위 필터링
    def test_apply_price_filter(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()
        search_page.apply_price_filter(min_price=50000, max_price=300000)
        search_page.should_have_search_results()

    # 정렬 테스트
    @pytest.mark.smoke
    def test_sort_by_price_low_to_high(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()
        search_page.sort_by_price_low_to_high()

    # 로그인 테스트
    @pytest.mark.login
    def test_login_from_search_page(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit()

        search_page = homepage.search_product("아이폰")
        search_page.should_be_on_search_page()

        search_page.click_login_button(test_account["id"], test_account["password"])

        # 로그인 상태에서도 검색 페이지 유지
        search_page.should_be_on_search_page()

    # 로그아웃 테스트
    @pytest.mark.login
    def test_logout_from_search_page(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit()

        search_page = homepage.search_product("갤럭시")

        # 로그인
        search_page.click_login_button(test_account["id"], test_account["password"])

        # 로그아웃 (홈페이지로 이동)
        home_page = search_page.logout()
        home_page.should_be_on_homepage()

    # 로고 클릭 테스트
    def test_return_to_home_via_logo(self, page):
        homepage = HomePage(page)
        homepage.visit()
        search_page = homepage.search_product("태블릿")

        search_page.click_logo()
        homepage.should_be_on_homepage()

    # 장바구니 테스트
    def test_cart_from_product_page(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit().should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        cart_page = search_page.click_cart_button()
        cart_page.should_be_on_cart_page()
