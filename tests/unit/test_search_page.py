import pytest

from framework.pages.home_page import HomePage


class TestSearchPageBasic:
    # should_be_on_search_page() 테스트
    @pytest.mark.smoke
    def test_search_page_loads_successfully(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("마우스")
        search_page.should_be_on_search_page()

    def test_should_be_on_search_page_no_results(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("존재하지않는상품12345abcde")
        result = search_page.should_be_on_search_page()

        assert result is search_page

    # should_have_search_results(min_results=1) 테스트
    @pytest.mark.smoke
    @pytest.mark.parametrize("keyword,min_results", [("마우스", 1), ("키보드", 10000)])
    def test_search_results_exist(self, page, keyword, min_results):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product(keyword)
        search_page.should_be_on_search_page()
        search_page.should_have_search_results(min_results)


class TestSearchPagePriceFilter:
    # apply_price_filter() 테스트
    @pytest.mark.slow
    @pytest.mark.parametrize("min_price, max_price", [(50000, 300000), (300000, 50000), (None, 300000), (100000, None)])
    def test_apply_price_filter(self, page, min_price, max_price):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()
        search_page.apply_price_filter(min_price=min_price, max_price=max_price)

    # apply_price_filter() 테스트(검색 결과 없음)
    @pytest.mark.slow
    def test_apply_price_filter_no_search(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("쉣숍")
        search_page.should_be_on_search_page()
        search_page.apply_price_filter(min_price=5000, max_price=500000)


class TestSearchPageSorting:
    # sort_by_price_low_to_high() 테스트
    @pytest.mark.smoke
    def test_sort_by_price_low_to_high(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()
        search_page.sort_by_price_low_to_high()

    # sort_by_price_low_to_high() 테스트(필터 후에)
    def test_sort_after_price_filter(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("키보드")
        search_page.should_be_on_search_page()

        search_page.apply_price_filter(min_price=30000, max_price=100000)

        search_page.sort_by_price_low_to_high()
        search_page.should_be_on_search_page()

    # sort_by_price_low_to_high() 테스트(연속동작)
    def test_sort_multiple_times(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("충전기")
        search_page.should_be_on_search_page()

        # 첫 번째 정렬
        search_page.sort_by_price_low_to_high()
        search_page.should_be_on_search_page()

        # 두 번째 정렬
        search_page.sort_by_price_low_to_high()
        search_page.should_be_on_search_page()


class TestSearchPageKeywordRelevance:
    # verify_search_keyword_in_results(keyword) 테스트
    @pytest.mark.smoke
    @pytest.mark.parametrize("keyword", ["타원", "무선 이어폰", "뭭뤡"])
    def test_search_keyword_relevance(self, page, keyword):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product(keyword)
        search_page.should_be_on_search_page()
        titles, is_relevant = search_page.verify_search_keyword_in_results(keyword)

        if titles:
            assert len(titles) > 0, f"{keyword} 검색 결과가 없습니다"

    # verify_search_keyword_in_results(keyword) 테스트(필터적용)
    def test_keyword_relevance_after_filter(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        keyword = "키보드"
        search_page = homepage.search_product(keyword)
        search_page.should_be_on_search_page()

        # 필터 적용
        search_page.apply_price_filter(min_price=20000, max_price=80000)

        # 필터 후 관련성 확인
        titles, is_relevant = search_page.verify_search_keyword_in_results(keyword)

        assert len(titles) > 0, "필터 후 검색 결과가 없습니다"

    # verify_search_keyword_in_results(keyword) 테스트(정렬적용)
    def test_keyword_relevance_after_sort(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        keyword = "마우스"
        search_page = homepage.search_product(keyword)
        search_page.should_be_on_search_page()

        search_page.sort_by_price_low_to_high()

        titles, is_relevant = search_page.verify_search_keyword_in_results(keyword)

        assert len(titles) > 0, "정렬 후 검색 결과가 없습니다"


class TestSearchPageProductTitles:
    # get_all_product_titles() 테스트
    @pytest.mark.parametrize("keyword", ["키보드", "졕쇈"])
    def test_get_all_product(self, page, keyword):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product(keyword)
        titles = search_page.get_all_product_titles()

        assert len(titles) >= 0, "상품 제목을 가져오지 못했습니다"
        assert len(titles) <= 10, "기본 제한(10개)을 초과했습니다"
        assert all(isinstance(title, str) for title in titles), "제목이 문자열이 아닙니다"
        assert all(len(title) > 0 for title in titles), "빈 제목이 있습니다"

    # get_all_product_titles() 테스트(2)
    @pytest.mark.parametrize("limit", [10, 11, 0])
    def test_get_all_product_titles_with_limit(self, page, limit):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("마우스")
        search_page.should_be_on_search_page()

        # 제한 개수로 상품 제목 가져오기
        titles = search_page.get_all_product_titles(limit)

        # 검증
        assert len(titles) >= 0, "상품 제목을 가져오지 못했습니다"
        assert len(titles) <= limit, f"제한({limit}개)을 초과했습니다"

    # get_all_product_titles() 테스트(필터적용)
    def test_get_all_product_titles_after_filter(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("헤드폰")
        search_page.should_be_on_search_page()

        # 필터 적용
        search_page.apply_price_filter(min_price=50000, max_price=200000)

        # 상품 제목 가져오기
        titles = search_page.get_all_product_titles(5)

        assert len(titles) >= 0, "필터 후 상품이 없습니다"

    # get_all_product_titles() 테스트(정렬적용)
    def test_get_all_product_titles_after_sort(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("모니터")
        search_page.should_be_on_search_page()

        # 정렬 적용
        search_page.sort_by_price_low_to_high()

        # 상품 제목 가져오기
        titles = search_page.get_all_product_titles(5)

        assert len(titles) >= 0, "정렬 후 상품이 없습니다"


class TestSearchPageProductInfo:
    #  get_product_title(index) 테스트
    @pytest.mark.parametrize("index", [1, 0, 10000])
    def test_get_product_title_multiple(self, page, index):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("키보드")
        search_page.should_be_on_search_page()

        # N번째 상품 정보 가져오기
        result = search_page.get_product_title(index)

        if result:
            title, price = result
            assert len(title) > 0, f"{index}번째 상품 제목이 비어있습니다"
            assert len(price) > 0, f"{index}번째 상품 가격이 비어있습니다"

    #  get_product_title(index) 테스트(필터적용)
    def test_get_product_title_after_price_filter(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("헤드셋")
        search_page.should_be_on_search_page()

        # 가격 필터 적용
        search_page.apply_price_filter(min_price=20000, max_price=80000)

        # 필터 후 상품 정보 가져오기
        result = search_page.get_product_title(1)

        assert result is not None, "필터 후 상품 정보를 가져올 수 없습니다"
        title, price = result

    #  get_product_title(index) 테스트(정렬적용)
    def test_get_product_title_after_sort(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("모니터")
        search_page.should_be_on_search_page()

        # 정렬 적용
        search_page.sort_by_price_low_to_high()

        # 정렬 후 상품 정보 가져오기
        result = search_page.get_product_title(1)

        assert result is not None, "정렬 후 상품 정보를 가져올 수 없습니다"
        title, price = result


class TestSearchPageClickProduct:
    # click_product_by_index(index) 테스트
    @pytest.mark.smoke
    @pytest.mark.parametrize("index", [1, 0, 10000])
    def test_click_multiple_products(self, page, index):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        product_page = search_page.click_product_by_index(index)
        if product_page:
            product_page.should_be_on_product_page()

    # click_product_by_index(index) 테스트(필터적용)
    def test_click_product_after_filter(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("키보드")
        search_page.should_be_on_search_page()

        # 필터 적용
        search_page.apply_price_filter(min_price=30000, max_price=100000)

        # 상품 클릭
        product_page = search_page.click_product_by_index(1)

        if product_page:
            product_page.should_be_on_product_page()

    # click_product_by_index(index) 테스트(정렬적용)
    def test_click_product_after_sort(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("헤드셋")
        search_page.should_be_on_search_page()

        # 정렬 적용
        search_page.sort_by_price_low_to_high()

        # 상품 클릭
        product_page = search_page.click_product_by_index(1)

        if product_page:
            product_page.should_be_on_product_page()


class TestSearchPageLogin:
    # click_login_button(username, password) 테스트
    @pytest.mark.login
    def test_login_from_search_page(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("아이폰")
        search_page.should_be_on_search_page()

        search_page.click_login_button(test_account["id"], test_account["password"])

        # 로그인 상태에서도 검색 페이지 유지
        search_page.should_be_on_search_page()

    # click_login_button(username,password) 테스트(잘못된 계정으로 로그인)
    @pytest.mark.login
    def test_invalid_login_search_page(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("포도")
        search_page.should_be_on_search_page()

        result = search_page.click_login_button("wrong_id", "wrong_password")

        assert not result, "로그인에 성공해서는 안됩니다"

    #  click_login_button(username,password) 테스트(로그인 상태)
    @pytest.mark.login
    def test_login_from_login_search_page(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("딸기")
        search_page.should_be_on_search_page()

        search_page.click_login_button(test_account["id"], test_account["password"])

        result = search_page.click_login_button(test_account["id"], test_account["password"])

        assert result is None, "로그인 실패"

    # logout() 테스트
    @pytest.mark.login
    def test_logout_from_search_page(self, page, test_account):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("갤럭시")
        search_page.should_be_on_search_page()

        search_page.click_login_button(test_account["id"], test_account["password"])

        # 로그아웃 (홈페이지로 이동)
        home_page = search_page.logout()
        home_page.should_be_on_homepage()

    # logout() 테스트(로그아웃 상태에서)
    @pytest.mark.login
    def test_logout_from_logout_search_page(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("밤")
        search_page.should_be_on_search_page()

        returned_searchpage = search_page.logout()

        assert not returned_searchpage, "로그아웃 성공"


class TestSearchPageNavigation:
    # click_logo() 테스트
    def test_return_to_home_via_logo(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("태블릿")
        search_page.should_be_on_search_page()

        homepage = search_page.click_logo()
        homepage.should_be_on_homepage()

    # click_cart_button() 테스트
    def test_cart_from_search_page(self, page):
        homepage = HomePage(page)
        homepage.visit()
        homepage.should_be_on_homepage()

        search_page = homepage.search_product("이어폰")
        search_page.should_be_on_search_page()

        cart_page = search_page.click_cart_button()
        cart_page.should_be_on_cart_page()
