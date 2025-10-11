# pages/search_page.py
import random

from playwright.sync_api import expect

from framework.base.base_page import BasePage
from framework.config.locators import SearchPageLocators


class SearchPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url_path = "/search"

    def should_be_on_search_page(self):
        """검색 결과 페이지에 있는지 확인"""
        print("검색 결과 페이지 확인")

        # 검색 결과 컨테이너 확인
        self.should_see_element(SearchPageLocators.SEARCH_CONTAINER)
        self.human_delay(0.3, 0.8)

        if self.page.locator(SearchPageLocators.NO_RESULT).is_visible():
            print("검색 결과가 없습니다")
            return self

        print(" 검색 결과 페이지 확인 완료")
        return self

    def should_have_search_results(self, min_results=1):
        """검색 결과가 있는지 확인 및 개수 반환"""
        print(f" 최소 {min_results}개 검색 결과 존재 확인")

        results = self.page.locator(SearchPageLocators.PRODUCT_CARDS)
        count = results.count()
        print(f" 검색 결과: {count}개 상품 발견")

        if count >= min_results:
            print(f" 검색 결과 확인: {count}개 상품")
            expect(results.first).to_be_visible(timeout=10000)
            return self
        else:
            print(f" 검색 결과 부족: {count}개 (최소 {min_results}개 필요) - URL: {self.page.url}")
            self.click_logo()
            return None

    def get_product_title(self, index):
        try:
            element = self.page.locator(SearchPageLocators.PRODUCT_CARDS).nth(index - 1)
            title_element = element.locator(SearchPageLocators.PRODUCT_TITLE)
            title = title_element.inner_text()
            print(f"상품명 : {title}")

            price_element = element.locator(SearchPageLocators.PRODUCT_PRICE)
            price = price_element.inner_text()
            print(f"상품가격 : {price}")

            return title, price
        except Exception as e:
            print(f"상품 가져오기 실패 : {e}")
            return None

    def click_product_by_index(self, index):
        try:
            product = self.page.locator(SearchPageLocators.PRODUCT_CARDS).nth(index - 1)

            if not product.is_visible():
                print(f"{index}번째 상품을 찾을 수 없습니다")
                return None

            img_element = product.locator(SearchPageLocators.PRODUCT_IMAGE)
            img_element.scroll_into_view_if_needed()
            self.human_delay(1, 2)

            with self.page.context.expect_page() as new_page_info:
                img_element.click()

            try:
                new_page = new_page_info.value
                new_page.wait_for_url("**/Item**", timeout=15000)
                print(f"새 페이지에서 동작 : {new_page.url}")

                from framework.pages.product_page import ProductPage

                return ProductPage(new_page)

            except Exception:
                print(f"현재 페이지에서 동작 : {self.page.url}")
                self.page.wait_for_url("**/Item**", timeout=15000)

                from framework.pages.product_page import ProductPage

                return ProductPage(self.page)

        except Exception as e:
            print(f"{index}번째 상품 클릭 실패: {e}")

            return None

    def apply_price_filter(self, min_price=None, max_price=None):
        try:
            price_filter = self.page.locator(SearchPageLocators.PRICE_FILTER)
            if price_filter:
                if min_price:
                    min_input = price_filter.locator(SearchPageLocators.FILTER_MIN)
                    min_input.type(str(min_price), delay=random.randint(20, 30))
                    self.human_delay(0.3, 0.5)

                if max_price:
                    max_input = price_filter.locator(SearchPageLocators.FILTER_MAX)
                    max_input.type(str(max_price), delay=random.randint(20, 30))
                    self.human_delay(0.3, 0.5)

                apply_btn = price_filter.locator(SearchPageLocators.FILTER_BUTTON)
                apply_btn.click()

                self.wait_for_load()

                print("가격 적용 완료")
            else:
                print("가격 필터 옵션을 찾을 수 없습니다")

        except Exception as e:
            print(f"가격 필터 적용 실패 : {e}")

    def sort_by_price_low_to_high(self):
        try:
            sort_dropdown = self.page.locator(SearchPageLocators.SORT_OPTIONS)
            sort_dropdown.click()

            self.human_delay(2, 4)

            low_to_high = self.page.locator('[aria-label="낮은 가격순"]')
            low_to_high.click()

            self.wait_for_load()

            print("가격 낮은 순 정렬 완료")

        except Exception as e:
            print(f"정렬 실패 : {e}")

    def get_all_product_titles(self, limit=10):
        """모든 상품명 리스트 반환 (제한된 개수)"""
        print(f" 상품명 리스트 수집 (최대 {limit}개)")

        titles = []
        try:
            products = self.page.locator(SearchPageLocators.PRODUCT_CARDS)
            count = min(products.count(), limit)

            for i in range(count):
                product = products.nth(i)
                title_element = product.locator(SearchPageLocators.PRODUCT_TITLE)
                title = title_element.inner_text()
                titles.append(title)

            print(f" {len(titles)}개 상품명 수집 완료")
            print(titles)
            return titles

        except Exception as e:
            print(f" 상품명 수집 실패: {e}")
            return titles

    def verify_search_keyword_in_results(self, keyword):
        """검색 키워드가 결과에 포함되는지 확인"""
        print(f" 검색어 '{keyword}' 관련성 확인")

        titles = self.get_all_product_titles(5)  # 상위 5개만 확인
        if titles:
            relevant_count = 0

            for title in titles:
                if keyword.lower() in title.lower():
                    relevant_count += 1
                    print(f"관련 상품: {title[:50]}...")
                else:
                    print(f"비관련 상품 : {title[:50]}...")

            relevance_rate = (relevant_count / len(titles)) * 100
            print(f" 관련성: {relevant_count}/{len(titles)} ({relevance_rate:.1f}%)")

            # 최소 30% 이상 관련성이 있어야 함
            if relevance_rate >= 30:
                print(" 검색 결과 관련성 양호")
                return titles, True
            else:
                print(f"️ 검색 결과 관련성 낮음: {relevance_rate:.1f}%")
                return titles, False
        else:
            print("검색 결과가 없습니다")
            return False

    def click_logo(self):
        print("쇼핑 계속하기")

        try:
            self.safe_click(SearchPageLocators.LOGO)
            print("메인 페이지로 이동")
            from framework.pages.home_page import HomePage

            return HomePage(self.page)

        except Exception as e:
            print(f"로고 클릭 실패: {e}")
            return False

    def click_login_button(self, username, password):
        print("로그인 버튼 클릭")

        try:
            login_btn = self.page.locator(SearchPageLocators.LOGIN_BUTTON)

            try:
                with self.page.context.expect_page(timeout=5000) as new_page_info:
                    login_btn.click()

                new_page = new_page_info.value
                new_page.wait_for_load_state("networkidle")

                from framework.pages.login_page import LoginPage

                login_page = LoginPage(new_page)
                login_page.should_be_on_login_page()

                # 자신(Search Page)을 전달
                if login_page.login(username, password):
                    return self
                else:
                    return None

            except Exception:
                # 현재 페이지에서 전환
                self.page.wait_for_load_state("networkidle")

                from framework.pages.login_page import LoginPage

                login_page = LoginPage(self.page)
                login_page.should_be_on_login_page()

                if login_page.login(username, password):
                    return self
                else:
                    return None

        except Exception as e:
            print(f"로그인 실패: {e}")
            return None

    def logout(self):
        print("로그아웃 시도")

        try:
            if not self.page.locator(SearchPageLocators.LOGOUT_BUTTON).is_visible():
                print("이미 로그아웃 상태입니다")
                return True

            self.safe_click(SearchPageLocators.LOGOUT_BUTTON)
            self.wait_for_load()

            print("로그아웃 완료")
            from framework.pages.home_page import HomePage

            return HomePage(self.page)

        except Exception as e:
            print(f"로그아웃 실패: {e}")

    def click_cart_button(self):
        """장바구니 버튼 클릭"""
        print("장바구니 버튼 클릭")
        self.safe_click(SearchPageLocators.CART_BUTTON)

        # 장바구니 페이지로 이동 대기
        self.page.wait_for_url("**/cart/**", timeout=10000)
        print("  ✓ 장바구니 페이지 이동")

        from framework.pages.cart_page import CartPage

        return CartPage(self.page)
