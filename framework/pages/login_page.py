from framework.base.base_page import BasePage
from framework.config.locators import LoginPageLocators


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        if page is None:
            raise ValueError("Page 객체가 None입니다. fixture를 확인하세요.")

    def should_be_on_login_page(self):
        print("로그인 페이지 확인")
        current_url = self.page.url
        assert "login" in current_url.lower(), f"로그인 페이지가 아닙니다: {current_url}"

        # 아이디 입력창 있는지 확인
        self.should_see_element(LoginPageLocators.ID_INPUT)
        print("로그인 페이지 확인 완료")
        return self

    def login(self, username, password):
        print(f"로그인 시도 {username}")

        try:
            # id입력
            self.safe_type(LoginPageLocators.ID_INPUT, username)

            # 비밀번호 입력
            self.safe_type(LoginPageLocators.PASSWORD_INPUT, password)

            # 로그인 버튼 클릭
            self.safe_click(LoginPageLocators.LOGIN_BUTTON)

            is_success = self.is_logged_in()
            if is_success:
                print(f"로그인 성공 :{is_success}")
            else:
                print(f"로그인 실패 : {is_success}")

            return is_success

        except Exception as e:
            print(f"로그인 실패: {e}")
            return False

    def is_logged_in(self):
        print("로그인 상태 확인")
        print(f"현재 URL: {self.page.url}")

        try:
            # 페이지 완전히 로드 대기
            self.page.wait_for_load_state("load", timeout=10000)

            # 추가 대기 (쿠키 적용 시간)
            self.human_delay(0.5, 1)

            # 로그아웃 버튼 찾기
            logout_btn = self.page.locator(LoginPageLocators.LOGOUT_BUTTON)

            count = logout_btn.count()
            print(f"매칭되는 요소 개수: {count}")

            # 10초간 기다림 (timeout 증가)

            logout_btn.wait_for(state="visible", timeout=10000)

            # 한 번 더 확인
            if logout_btn.is_visible():
                print("로그인 상태입니다")
            else:
                print("로그아웃 버튼이 보이지 않음")
            return logout_btn.is_visible()

        except Exception as e:
            print(f"❌ 로그인 상태 확인 실패: {e}")
            self.page.screenshot(path="is_logged_in_error.png")
            return False
