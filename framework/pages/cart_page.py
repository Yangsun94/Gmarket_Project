from playwright.sync_api import expect

from framework.base.base_page import BasePage
from framework.config.locators import CartPageLocators


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url_path = "/cart/"

    def should_be_on_cart_page(self):
        print("장바구니 페이지 확인")

        current_url = self.page.url
        if "cart" in current_url.lower():
            print(f"장바구니 페이지 URL 확인 : {current_url}")

        self.should_see_element(CartPageLocators.CART_CONTAINER)
        self.human_delay(0.3, 0.8)

        print("장바구니 페이지 확인 완료")
        return self

    def get_cart_items(self):
        print("장바구니 상품 목록 수집")

        items = []
        try:
            cart_items = self.page.locator(CartPageLocators.CART_ITEMS)
            count = cart_items.count()

            if count == 0:
                print("장바구니가 비었습니다")
                return items

            print(f"총 {count}개 상품 발견")

            for i in range(count):
                item = cart_items.nth(i)
                try:
                    title = item.locator(CartPageLocators.ITEM_TITLE).inner_text()
                    price = item.locator(CartPageLocators.ITEM_PRICE).inner_text()

                    items.append({"index": i + 1, "title": title, "price": price})
                    print(f"{i+1}번째 상품, {title}, {price}")

                except Exception as e:
                    print(f"요소를 찾지 못했습니다: {e}")

        except Exception as e:
            raise Exception(f"에러가 발생했습니다: {e}")

        print(f"총 {len(items)}개 상품 정보 수집")
        return items

    def remove_item(self, index=1):
        print(f"{index}번째 상품 제거 시도")

        try:
            items = self.get_cart_items()
            if len(items) < index:
                raise IndexError(f"제거 할 수 없습니다: {index}번째 상품이 없음")

            # 다이얼로그 자동 수락 설정
            self.page.on("dialog", lambda dialog: dialog.accept())

            remove_btn = self.page.locator(CartPageLocators.ITEM_REMOVE)
            remove_btn.nth(index - 1).scroll_into_view_if_needed()
            self.human_delay(1, 2)
            remove_btn.nth(index - 1).click()

            self.human_delay(1, 2)
            print(f"{index}번째 상품 제거 완료")
            return True
        except Exception as e:
            print(f"상품 제거 실패: {e}")

    def clear_cart(self):
        print("장바구니 전체 비우기")

        try:
            checkbox = self.page.locator(CartPageLocators.CHECKBOX)
            if not checkbox.is_visible():
                print("장바구니가 이미 비어있습니다.")
                return True
            checkbox.check()
            self.human_delay(1, 2)

            # 다이얼로그 자동 수락 설정
            self.page.on("dialog", lambda dialog: dialog.accept())

            clear_btn = self.page.locator(CartPageLocators.ITEM_REMOVE_ALL)
            clear_btn.click()

            self.human_delay(1, 2)
            print("전체 삭제 완료")
            return True

        except Exception as e:
            print(f"전체 삭제 실패: {e}")
            return False

    def update_quantity(self, index, quantity):
        print(f"{index}번째 상품을 {quantity}개로 변경")

        try:
            items = self.get_cart_items()
            if len(items) < index:
                raise IndexError(f"변경 할 수 없습니다: {index}번째 상품이 없음")

            quantity_btn = self.page.locator(CartPageLocators.QUANTITY)
            quantity_plus = self.page.locator(CartPageLocators.QUANTITY_PLUS)
            quantity_minus = self.page.locator(CartPageLocators.QUANTITY_MINUS)

            quantity_value = int(quantity_btn.nth(index - 1).get_attribute("value"))
            print(f"현재 수량: {quantity_value}, 목표 수량: {quantity}")

            while quantity_value < quantity:
                quantity_plus.nth(index - 1).click()
                self.human_delay(1, 2)
                quantity_value = int(quantity_btn.nth(index - 1).get_attribute("value"))

            while quantity_value > quantity:
                quantity_minus.nth(index - 1).click()
                self.human_delay(1, 2)
                quantity_value = int(quantity_btn.nth(index - 1).get_attribute("value"))

            print(f"수량 변경 완료: {quantity_value}")

            return True

        except Exception as e:
            print(f"수량 변경 실패: {e}")
            return False

    def get_total_price(self):
        print("총 결제 금액 가져오기")

        try:
            item_info = self.page.locator(CartPageLocators.ORDER_SUMMARY)

            discount = item_info.locator(CartPageLocators.DISCOUNT_AMOUNT)
            price = item_info.locator(CartPageLocators.SHIPPING_FEE)
            item_price = price.nth(0)
            shipping_fee = price.nth(1)

            total_price = item_info.locator(CartPageLocators.TOTAL_PRICE)

            print(
                f"상품가격: {item_price.inner_text()} + 배송비: {shipping_fee.inner_text()}- 할인: {discount.inner_text()}"
                f"=총 가격: {total_price.inner_text()}"
            )

            return total_price.inner_text()

        except Exception as e:
            print(f"총 금액 확인 실패: {e}")
            return None

    def click_logo(self):
        print("쇼핑 계속하기")

        try:
            self.safe_click(CartPageLocators.LOGO)
            print("로고 클릭으로 홈페이지로 이동")
            from framework.pages.home_page import HomePage

            return HomePage(self.page)

        except Exception as e:
            print(f"로고 클릭 실패: {e}")
            return None

    def proceed_to_checkout(self):
        print("결제 페이지로 이동")

        try:
            checkout_btn = self.page.locator(CartPageLocators.CHECKOUT_BUTTON)

            expect(checkout_btn).to_be_visible()
            expect(checkout_btn).to_be_enabled()

            checkout_btn.scroll_into_view_if_needed()
            self.human_delay(1, 2)
            checkout_btn.click()

            self.page.wait_for_url("**/checkout**", timeout=15000)
            print("결제 페이지 이동 완료")
            self.human_delay(0.3, 0.8)

        except Exception as e:
            print(f"결제 페이지 이동 실패: {e}")
            return None

    def click_login_button(self, username, password):
        print("로그인 버튼 클릭")

        try:
            login_btn = self.page.locator(CartPageLocators.LOGIN_BUTTON)

            try:
                with self.page.context.expect_page(timeout=5000) as new_page_info:
                    login_btn.click()

                new_page = new_page_info.value
                new_page.wait_for_load_state("networkidle")

                from framework.pages.login_page import LoginPage

                login_page = LoginPage(new_page)
                login_page.should_be_on_login_page()

                # 자신(CartPage)을 전달
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
            if not self.page.locator(CartPageLocators.LOGOUT_BUTTON).is_visible():
                print("이미 로그아웃 상태입니다")
                return True

            self.safe_click(CartPageLocators.LOGOUT_BUTTON)
            self.wait_for_load()

            print("로그아웃 완료")
            from framework.pages.home_page import HomePage

            return HomePage(self.page)

        except Exception as e:
            print(f"로그아웃 실패: {e}")
