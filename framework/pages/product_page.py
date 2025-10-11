from framework.base.base_page import BasePage
from framework.config.locators import ProductPageLocators


class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url_path = "/item"

    def should_be_on_product_page(self):
        print("상품 상세 페이지에 있는지 확인")

        # 상품 정보 컨테이너 있는지 확인
        self.should_see_element(ProductPageLocators.PRODUCT_CONTAINER)
        self.human_delay(0.3, 0.8)

        print("상품 상세 페이지 확인 완료")
        return self

    def get_product_info(self):
        print("상품 정보 수집")

        try:
            # 상품명
            title_element = self.page.locator(ProductPageLocators.PRODUCT_TITLE)
            print(title_element.is_visible())
            title = title_element.inner_text()

            # 가격
            price_element = self.page.locator(ProductPageLocators.PRODUCT_PRICE)

            if price_element.count() >= 2:
                price = price_element.nth(1).inner_text()
            else:
                price = price_element.nth(0).inner_text()

            # 배송 정보
            shipping_element = self.page.locator(ProductPageLocators.SHIPPING_INFO)

            if shipping_element.count() >= 2:
                shipping = shipping_element.nth(1).inner_text()
            else:
                shipping = shipping_element.nth(0).inner_text()

            product_info = {
                "title": title,
                "price": price,
                "shipping": shipping,
            }

            print(f" 상품명: {title[:50]}...")
            print(f" 가격: {price}")
            print(f" 배송: {shipping}")

            return product_info

        except Exception as e:
            print(f" 상품 정보 수집 실패: {e}")
            return None

    def scroll_and_explore(self):
        print("상품 페이지 탐색")

        try:
            # 페이지 중간까지 스크롤
            self.page.evaluate("window.scrollTo(0, window.innerHeight)")
            self.human_delay(1, 2)

            # 페이지 하단까지 스크롤
            self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            self.human_delay(1, 2)

            # 페이지 상단까지 스크롤
            self.page.evaluate("window.scrollTo(0, 0)")
            self.human_delay(0.5, 1)

            print("페이지 탐색 완료")

        except Exception as e:
            print(f"페이지 탐색 실패 : {e}")

    def add_to_cart(self, quantity=1):
        print(f"수량 {quantity}개로 장바구니에 담기")

        try:
            option_btn = self.page.locator(ProductPageLocators.OPTION_BUTTON)
            option_dropdown = self.page.locator(ProductPageLocators.OPTION_DROPDOWN)
            available_options = False

            # 옵션 선택창이 있다면 선택
            if option_btn.count() > 0:
                option_btn.click()
                self.human_delay(0.3, 0.5)

                for i in range(option_dropdown.count()):
                    # 매진 확인
                    if "soldout" in option_dropdown.nth(i).get_attribute("class"):
                        continue

                    # 구매 가능한 옵션 선택
                    option_dropdown.nth(i).click()
                    self.human_delay(0.3, 0.5)
                    available_options = True
                    break

                # 모든 옵션이 매진인 경우
                if not available_options:
                    print("모든 옵션이 품절입니다")
                    option_btn.click()
                    return False

            # 수량 증가
            for selector in ProductPageLocators.PRODUCT_PLUS:
                if self.page.locator(selector).count() > 0:
                    plus_btn = self.page.locator(selector).first
                    break
            current = 1

            while current < quantity:
                plus_btn.click()
                self.human_delay(0.3, 0.5)
                current += 1

            # 선택 버튼이 있으면 클릭
            select_btn = self.page.locator(ProductPageLocators.PRODUCT_SELECT).first
            if select_btn.count() > 0:
                select_btn.click()
                self.human_delay(0.3, 0.5)

            # 장바구니 담기
            add_cart = self.page.locator(ProductPageLocators.ADD_CART)
            add_cart.click()
            self.human_delay(1, 2)

            # 팝업 닫기
            popup_btn = self.page.locator(ProductPageLocators.POPUP_BUTTON)
            if popup_btn.count() > 0 and popup_btn.is_visible(timeout=3000):
                popup_btn.click(force=True)
                self.human_delay(0.3, 0.5)

            print("장바구니 담기 성공")
            return True

        except Exception as e:
            print(f"장바구니 담기 실패: {e}")
            return False

    def click_logo(self):
        print("쇼핑 계속하기")

        try:
            self.safe_click(ProductPageLocators.LOGO)
            print("메인 페이지로 이동")
            from framework.pages.home_page import HomePage

            return HomePage(self.page)

        except Exception as e:
            print(f"로고 클릭 실패: {e}")
            return False

    def click_cart_button(self):
        """장바구니 버튼 클릭"""
        print("장바구니 버튼 클릭")
        self.safe_click(ProductPageLocators.CART_BUTTON)

        # 장바구니 페이지로 이동 대기
        self.page.wait_for_url("**/cart/**", timeout=10000)
        print("  ✓ 장바구니 페이지 이동")

        from framework.pages.cart_page import CartPage

        return CartPage(self.page)

    def click_login_button(self, username, password):
        print("로그인 버튼 클릭")

        try:
            login_btn = self.page.locator(ProductPageLocators.LOGIN_BUTTON)

            try:
                with self.page.context.expect_page(timeout=5000) as new_page_info:
                    login_btn.click()

                new_page = new_page_info.value
                new_page.wait_for_load_state("networkidle")

                from framework.pages.login_page import LoginPage

                login_page = LoginPage(new_page)
                login_page.should_be_on_login_page()

                # 자신(ProductPage)을 전달
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
            if not self.page.locator(ProductPageLocators.LOGOUT_BUTTON).is_visible():
                print("이미 로그아웃 상태입니다")
                return True

            self.safe_click(ProductPageLocators.LOGOUT_BUTTON)
            self.wait_for_load()

            print("로그아웃 완료")
            from framework.pages.home_page import HomePage

            return HomePage(self.page)

        except Exception as e:
            print(f"로그아웃 실패: {e}")

    def goto_product(self):
        self.page.goto("https://item.gmarket.co.kr/Item?goodscode=4070837165")
        return self
