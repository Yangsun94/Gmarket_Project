#pages/home_page.py

import pytest

from framework.base.base_page import BasePage
from framework.config.locators import GmarketLocators, SearchPageLocators
from playwright.sync_api import expect

from framework.pages.search_page import SearchPage


#G마켓 홈페이지 클래스
class HomePage(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.url_path = ""



    def visit(self):
        print("G마켓 홈페이지 방문")
        self.goto(self.url_path)
        return self

    def should_be_on_homepage(self):
        print("홈페이지 도달 확인")

        self.human_delay(0.3, 0.8)
        self.should_have_url("https://www.gmarket.co.kr/")

        current_title = self.get_page_title()
        print(current_title)
        if "G마켓" not in current_title and "gmarket" not in current_title.lower():
            raise AssertionError(f"홈페이지가 아닙니다. 현재 제목 : {current_title}")

        #로고 확인
        self.should_see_element(GmarketLocators.LOGO)
        print("홈페이지 도달 확인 완료")
        return self

    #홈페이지 주요 요소들 보이는지 확인
    def should_see_main_elements(self):
        print("홈페이지 주요 요소 확인")

        #헤더 확인
        self.should_see_element(GmarketLocators.HEADER)
        print("헤더 표시됨")
        #로고 확인
        self.should_see_element(GmarketLocators.LOGO)
        print("로고 표시됨")
        #검색창 확인
        self.should_see_element(GmarketLocators.SEARCH_INPUT)
        print("검색창 표시됨")
        #검색 버튼 확인
        self.should_see_element(GmarketLocators.SEARCH_BUTTON)
        print("검색 버튼 표시 됨")

        print("주요 요소 확인됨")
        return self

    #상품 검색
    def search_product(self,keyword):
        print(f"상품 검색 : '{keyword}'")

        #검색창에 키워드 입력
        self.safe_type(GmarketLocators.SEARCH_INPUT,keyword)
        print(f"검색어 입력 : '{keyword}'")

        #검색버튼 클릭
        self.safe_click(GmarketLocators.SEARCH_BUTTON)

        #검색 결과 페이지로 이동될 때까지 대기
        self.page.wait_for_url('**/search**',timeout=15000)
        print("검색 결과 페이지로 이동 완료")

        #SearchPage객체 반환
        from framework.pages.search_page import SearchPage
        return SearchPage(self.page)


    #엔터키로 검색
    def search_with_enter(self,keyword):
        print(f"Enter 키로 검색 : {keyword}")

        self.safe_click(GmarketLocators.SEARCH_INPUT)
        self.safe_type(GmarketLocators.SEARCH_INPUT,keyword,clear=True)

        self.safe_press("Enter")
        print("Enter 키 입력")

        #검색 결과 페이지 대기
        self.page.wait_for_url('**/search**',timeout=15000)
        print("검색결과 페이지 이동 완료")

        #SearchPage객체 반환
        from framework.pages.search_page import SearchPage
        return SearchPage(self.page)

    def should_see_search_suggestions(self):
        """검색 자동완성이 나타나는지 확인"""
        print(" 검색 자동완성 확인")

        # 자동완성 목록이 보이는지 확인
        suggestions = self.page.locator(GmarketLocators.SEARCH_SUGGESTION)
        expect(suggestions).to_be_visible(timeout=5000)

        print(" 자동완성 목록 표시됨")
        return self

    def type_in_search_without_submit(self, keyword):
        """검색만 입력하고 제출하지 않음 (자동완성 테스트용)"""
        print(f" 검색어만 입력: '{keyword}'")

        self.safe_type(GmarketLocators.SEARCH_INPUT, keyword, clear=True)

        # 자동완성이 나타날 시간을 줌
        self.human_delay(1, 2)
        return self

    # ==============================================
    # 🔗 네비게이션 기능
    # ==============================================

    def click_logo(self):
        print("쇼핑 계속하기")

        try:
            self.safe_click(SearchPageLocators.LOGO)
            self.should_see_element('#comp_24948199')
            print("추천픽 페이지로 이동")
            return True

        except Exception as e:
            print(f"로고 클릭 실패: {e}")
            return False

    def click_login_button(self,username,password):
        print("로그인 버튼 클릭")

        try:
            login_btn = self.page.locator(GmarketLocators.LOGIN_BUTTON)

            try:
                with self.page.context.expect_page(timeout=5000) as new_page_info:
                    login_btn.click()

                new_page = new_page_info.value
                new_page.wait_for_load_state('networkidle')

                from framework.pages.login_page import LoginPage
                login_page = LoginPage(new_page)
                login_page.should_be_on_login_page()

                # 자신(HomePage)을 전달
                if login_page.login(username, password):
                    return self
                else:
                    return None

            except:
                # 현재 페이지에서 전환
                self.page.wait_for_load_state('networkidle')

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
            if not self.page.locator(GmarketLocators.LOGOUT_BUTTON).is_visible():
                print("이미 로그아웃 상태입니다")
                return False

            self.safe_click(GmarketLocators.LOGOUT_BUTTON)
            self.wait_for_load()

            print("로그아웃 완료")
            return HomePage(self.page)

        except Exception as e:
            print(f"로그아웃 실패: {e}")

    def click_cart_button(self):
        """장바구니 버튼 클릭"""
        print("장바구니 버튼 클릭")
        self.safe_click(GmarketLocators.CART_BUTTON)

        # 장바구니 페이지로 이동 대기
        self.page.wait_for_url("**/cart/**", timeout=10000)
        print("  ✓ 장바구니 페이지 이동")

        from framework.pages.cart_page import CartPage
        return CartPage(self.page)

    # ==============================================
    # 🎭 사용자 행동 시뮬레이션
    # ==============================================

    def browse_homepage_naturally(self):
        """홈페이지를 자연스럽게 둘러보기"""
        print("홈페이지 자연스럽게 둘러보기")

        # 페이지 로딩 후 잠시 대기
        self.human_delay(0.3, 0.8)

        # 스크롤하면서 둘러보기
        self.simulate_reading()

        # 가끔 마우스 움직임
        self.simulate_mouse_movement()
        self.human_delay(1, 2)

        # 다시 상단으로
        self.page.evaluate("window.scrollTo(0, 0)")
        self.human_delay(1, 2)

        print("자연스러운 브라우징 완료")
        return self

    def hover_over_categories(self):
        """카테고리에 마우스 올려보기"""
        print("카테고리 메뉴 hover")

        try:
            category_menu = self.page.locator(GmarketLocators.CATEGORY_MENU)
            count = category_menu.count()
            print(f"카테고리 메뉴 개수: {count}")

            # 각 요소를 개별적으로 확인
            for i in range(count):
                element = category_menu.nth(i)
                try:
                    # 각 요소의 정보 출력
                    text_content = element.text_content()
                    is_visible = element.is_visible()
                    print(f"Element {i}: visible={is_visible}, text='{text_content[:50]}...'")

                    # 첫 번째로 보이는 요소에 hover
                    if is_visible:  # 또는 원하는 조건
                        element.hover()
                        self.human_delay(1, 2)
                        print(f"  ✓ 카테고리 메뉴 hover 완료 (index: {i})")
                except Exception as e:
                    print(f"Element {i} 처리 중 오류: {e}")
                    continue
            else:
                print("  ️ hover 가능한 카테고리 메뉴를 찾을 수 없음")

        except Exception as e:
            print(f"카테고리 hover 중 오류: {e}")

        return self


    # ==============================================
    # 유틸리티 메서드
    # ==============================================

    def get_search_input_placeholder(self):
        """검색창의 placeholder 텍스트 가져오기"""
        search_input = self.page.locator(GmarketLocators.SEARCH_INPUT)
        try:
            placeholder = search_input.get_attribute("placeholder")
            print(f"🔍 검색창 placeholder: '{placeholder}'")
            return placeholder
        except Exception as e:
            print(f"요소 찾기 실패 : {e}")

    def is_login_button_visible(self):
        """로그인 버튼이 보이는지 확인 (로그인 상태 체크용)"""
        try:
            login_btn = self.page.locator(GmarketLocators.LOGIN_BUTTON)
            is_visible = login_btn.is_visible()
            status = "로그아웃 상태" if is_visible else "로그인 상태"
            print(f"현재 상태: {status}")
            return is_visible
        except:
            return True  # 에러 시 로그아웃 상태로 가정

    def wait_for_page_load(self):
        """페이지 완전 로딩 대기"""
        print("페이지 로딩 대기")

        # 네트워크 유휴 상태까지 대기
        self.wait_for_load()

        # 주요 요소들이 보일 때까지 대기
        self.page.wait_for_selector(GmarketLocators.SEARCH_INPUT, timeout=15000)

        # 추가 안정화 시간
        self.human_delay(2, 3)

        print("  페이지 로딩 완료")
        return self

    # ==============================================
    #  테스트 지원 메서드
    # ==============================================

    def capture_homepage_screenshot(self, name="homepage"):
        """홈페이지 스크린샷 촬영"""
        screenshot_name = f"{name}_{self.page.url.replace('https://', '').replace('/', '_')}"
        return self.take_screenshot(screenshot_name)

    def verify_no_errors(self):
        """페이지 오류가 없는지 확인"""
        print("페이지 오류 확인")

        # 일반적인 오류 메시지들 확인
        error_messages = [
            "error", "오류", "문제가 발생", "접속 불가",
            "service unavailable", "502", "503", "404"
        ]

        page_text = self.page.locator('body').inner_text().lower()

        for error_msg in error_messages:
            if error_msg in page_text:
                print(f"오류 발견: {error_msg}")
                self.take_screenshot(f"error_{error_msg}")
                raise AssertionError(f"페이지에서 오류 발견: {error_msg}")

        print("오류 없음")
        return self



