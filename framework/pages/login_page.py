from framework.base.base_page import BasePage
from framework.config.locators import LoginPageLocators
from playwright.sync_api import expect

class LoginPage(BasePage):

    def __init__(self,page):
        super().__init__(page)

    def should_be_on_login_page(self):
        print("로그인 페이지 확인")
        current_url = self.page.url
        assert 'login' in current_url.lower(),f"로그인 페이지가 아닙니다: {current_url}"

        #아이디 입력창 있는지 확인
        self.should_see_element(LoginPageLocators.ID_INPUT)
        print("로그인 페이지 확인 완료")
        return self


    def login(self,username,password):
        print(f"로그인 시도 {username}")

        try:
            #id입력
            self.safe_type(LoginPageLocators.ID_INPUT,username)

            #비밀번호 입력
            self.safe_type(LoginPageLocators.PASSWORD_INPUT,password)

            #로그인 버튼 클릭
            self.safe_click(LoginPageLocators.LOGIN_BUTTON)
            self.wait_for_load()

            if self.is_logged_in():
                print("로그인 성공")
                return True

            print("로그인 실패")
            return False


        except Exception as e:
            print(f"로그인 실패: {e}")
            return None


    def is_logged_in(self):
        print("로그인 상태 확인")

        try:
            logout_btn = self.page.locator(LoginPageLocators.LOGOUT_BUTTON)

            if logout_btn.is_visible(timeout=3000):
                print("로그인 상태입니다")
                return True
            else:
                print("로그아웃 상태입니다")
                return False

        except Exception as e:
            print(f"로그인 상태 확인 실패: {e}")
            return False