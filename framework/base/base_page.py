# base/base_page.py

from playwright.sync_api import Page, expect
import time
import random

class BasePage(Page):
    def __init__(self,page:Page):
        self.page = page
        self.base_url = "https://gmarket.co.kr"

    # ==============================================
    #페이지 네비게이션
    # ==============================================

    def goto(self,path=""):

        url = f"{self.base_url}{path}" if path else self.base_url
        print(f"페이지 이동 : {url}")

        self.page.goto(url,wait_until="domcontentloaded")

        return self

    # 페이지 완전 로딩대기
    def wait_for_load(self,timeout=30000):

        self.page.wait_for_load_state("networkidle", timeout=timeout)
        return self


    # ==============================================
    #요소 찾기 및 대기
    # ==============================================


    # 요소 찾기(대기 포함)
    def find_element(self,selector,timeout=10000):

        try:
            return self.page.locator(selector,timeout=timeout)
        except Exception as e:
            print(f"요소를 찾을 수 없습니니다 {selector}")
            raise e

    def find_elements(self,selector):
        return self.page.locator(selector).all()


    # 요소가 보일때까지 대기
    def wait_for_element_visible(self,selector,timeout=10000):
        element = self.page.locator(selector)
        expect(element).to_be_visible(timeout=timeout)
        return element

    # 요소가 사라질때까지 대기
    def wait_for_element_hidden(self,selector,timeout=10000):

        element = self.page.locator(selector)
        expect(element).to_be_hidden(timeout=timeout)
        return element


    # ==============================================
    # 사용자 액션 (자연스러운 동작)
    # ==============================================


    # 요소대기 + 자연스러운 동작
    def safe_click(self,selector,timeout=10000):

        print(f"클릭 : {selector}")

        self.page.wait_for_selector(selector,timeout=timeout)
        element = self.page.locator(selector)
        expect(element).to_be_visible(timeout=timeout)


        element.hover()
        time.sleep(random.uniform(0.2,0.5))

        element.click()
        time.sleep(random.uniform(0.3,0.8))

        return self

    # 자연스러운 타이핑
    def safe_type(self,selector,text,clear=True, delay_range=(50,150)):

        print(f"텍스트 입력 : {selector} -> '{text}'")

        self.page.wait_for_selector(selector)
        element = self.page.locator(selector)
        expect(element).to_be_visible()

        if clear:
            element.click()
            self.page.keyboard.press("Control+a")
            time.sleep(0.1)

        element.type(text, delay=random.randint(*delay_range))
        time.sleep(random.uniform(0.3, 0.8))
        return self

    # 안전한 키 입력
    def safe_press(self, key):
        print(f"키 입력 : {key}")
        self.page.keyboard.press(key)
        time.sleep(random.uniform(0.5, 1.0))
        return self

    # 자연스러운 딜레이
    def human_delay(min_seconds=1, max_seconds=3):
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    # ==============================================
    #  검증 메서드
    # ==============================================

    #페이지 타이틀 검증
    def should_have_title(self,expected_title):
        expect(self.page).to_have_title(expected_title)
        return self

    #페이지 url 검증
    def should_have_url(self,expected_url):
        expect(self.page).to_have_url(expected_url)
        return self

    #요소 존재 검증
    def should_see_element(self,selector):
        element = self.page.locator(selector)
        expect(element).to_be_visible()
        return self

    #요소 부재 검증
    def should_not_see_element(self,selector):
        element = self.page.locator(selector)
        expect(element).not_to_be_visible()
        return self

    #텍스트 존재 검증
    def should_see_text(self,text,selector=None):
        if selector:
            element = self.page.locator(selector)
            expect(element).to_contain_text(text)
        else:
            expect(self.page.locator('body')).to_contain_text(text)

        return self

    # ==============================================
    #자연스러운 행동 시뮬레이션
    # ==============================================

    #사람처럼 자연스러운 딜레이
    def human_delay(self,min_delay=1,max_delay=3):
        delay = random.uniform(min_delay,max_delay)
        time.sleep(delay)
        return self

    #페이지 읽는것같은 행동
    def simulate_reading(self):
        print("페이지 읽는중")

        self.page.evaluate("window.scrollTo(0,0)")
        time.sleep(random.uniform(1,2))

        for _ in range(random.randint(2, 4)):
            scroll_distance = random.randint(200,500)
            self.page.evaluate(f"window.scrollBy(0,{scroll_distance})")
            time.sleep(random.uniform(0.8,2.0))
            return self

    #자연스러운 마우스 움직임
    def simulate_mouse_movement(self):
        viewport = self.page.viewport_size
        x = random.randint(100, viewport['width'] - 100)
        y = random.randint(100, viewport['height'] - 100)

        self.page.mouse.move(x,y)
        time.sleep(random.uniform(0.2,0.5))
        return self

    # ==============================================
    # 유틸리티 메서드
    # ==============================================

    #스크린샷 촬영
    def take_screenshot(self,name=None):
        if name is None:
            name = f"screenshot_{int(time.time())}"

        path = f"reports/screenshots/{name}.png"
        self.page.screenshot(path=path)
        print(f"스크린샷 저장 : {path}")
        return self

    #url 반환
    def get_current_url(self):
        return self.page.url

    #페이지 타이틀 반환
    def get_page_title(self):
        return self.page.title()

    #페이지 새로고침
    def refresh_page(self):
        print("페이지 새로고침")
        self.page.reload()
        time.sleep(random.uniform(2,4))
        return self

    #요소까지 스크롤
    def scroll_to_element(self,selector):
        element = self.page.locator(selector)
        element.scroll_into_view_if_needed()
        time.sleep(random.uniform(0.5,1.0))
        return self
