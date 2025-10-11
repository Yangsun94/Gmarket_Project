#config/locators.py


#G마켓 메인 페이지 selector들
class GmarketLocators:

    #로그인 관련
    LOGIN_BUTTON = 'a:has-text("로그인")'
    LOGOUT_BUTTON = 'a:has-text("로그아웃")'

    #헤더 영역
    HEADER = "#header"
    LOGO = ".link__head"
    CART_BUTTON = "li.list-item.list-item--cart"

    #검색 영역
    SEARCH_INPUT = "input[name= 'keyword']"
    SEARCH_BUTTON = "button[type='submit']"
    SEARCH_SUGGESTION = "#skip-navigation-search"

    #네비게이션
    CATEGORY_MENU = "#box__category-all-layer > ul > li.list-item__1depth > a"

#검색 결과 페이지 selector들
class SearchPageLocators:

    LOGO = ".link__head"
    CART_BUTTON = "li.list-item.list-item--cart"

    # 로그인 관련
    LOGIN_BUTTON = 'a:has-text("로그인")'
    LOGOUT_BUTTON = 'a:has-text("로그아웃")'

    #검색 결과 컨테이너
    SEARCH_CONTAINER = "#container"
    NO_RESULT = ".box__ment"

    #개별 상품 카드
    PRODUCT_CARDS = ".box__component.box__component-itemcard.box__component-itemcard--general"
    PRODUCT_TITLE = "span.text__item"
    PRODUCT_PRICE = "strong.text.text__value"
    PRODUCT_IMAGE = "img.image__item"

    #필터 및 정렬
    SORT_OPTIONS = ".button__toggle-sort"
    PRICE_FILTER = ".box__component.box__component-filter.box__component-price-filter"
    FILTER_MIN = "input[placeholder*='최소']"
    FILTER_MAX = "input[placeholder*='최대']"
    FILTER_BUTTON = "button.button__filter-price.montelena-post"


#검색 상세 페이지 selector들
class ProductPageLocators:

    # 로그인 관련
    LOGIN_BUTTON = 'a:has-text("로그인")'
    LOGOUT_BUTTON = 'a:has-text("로그아웃")'

    # 기본 컨테이너 및 헤더
    LOGO = ".link__head"
    PRODUCT_CONTAINER = "#container"
    CART_BUTTON = "li.list-item.list-item--cart"

    # 배송 정보
    SHIPPING_INFO = ".box__txt-information"

    # 상품 기본 정보
    PRODUCT_TITLE = ".box__item-info > h1"
    PRODUCT_PRICE = "span.price_innerwrap > strong.price_real"
    PRODUCT_IMAGES = ".box__viewer-container"

    # 페이지 기능
    OPTION_BUTTON = "#optOrderSel_0 > button.select-item_option.uxeselect_btn"
    OPTION_DROPDOWN = "#optOrderSel_0 > ul > li"
    PRODUCT_PLUS = [".bt_increase", ".bt_increase.uxeselect_btn"]
    PRODUCT_SELECT = ".bt_select.uxeselect_btn"
    ADD_CART = "#coreAddCartBtn"

    #팝업
    POPUP_BUTTON = ".btn_round.btn_gray"


#장바구니 페이지 selector들
class CartPageLocators:

    # 로그인 관련
    LOGIN_BUTTON = 'a:has-text("로그인")'
    LOGOUT_BUTTON = 'a:has-text("로그아웃")'

    # 컨테이너 및 로고
    CART_CONTAINER = "#container"
    LOGO = "h1.box__title-logo > a"

    # 장바구니 아이템
    CART_ITEMS = ".shipping--no--group"
    ITEM_IMAGE = "div.item_img > a"
    ITEM_TITLE = "div.section.item_title > a"
    ITEM_PRICE = "div.section.item_price"

    # 수량 조절
    QUANTITY = ".item_qty_count"
    QUANTITY_PLUS = ".btn_plus.sprite__cart"
    QUANTITY_MINUS = ".btn_minus.sprite__cart"

    # 삭제 버튼
    CHECKBOX = "#item_all_select"
    ITEM_REMOVE = ".icon.sprite__cart.btn_cart_item_del"
    ITEM_REMOVE_ALL = 'span:has-text("선택삭제")'

    # 주문 요약
    ORDER_SUMMARY = "#cart_order"
    TOTAL_PRICE = ".order_summary > span.format-price"
    DISCOUNT_AMOUNT = ".format-price.discount > span.box__format-amount"
    SHIPPING_FEE = "span.format-price > span"

    # 체크아웃
    CHECKOUT_BUTTON = "button.btn_submit"

#로그인 페이지 selector들
class LoginPageLocators:

    # 아이디 입력
    ID_INPUT = "#typeMemberInputId"

    # 비밀번호 입력
    PASSWORD_INPUT = "#typeMemberInputPassword"

    # 로그인 버튼
    LOGIN_BUTTON = "#btn_memberLogin"

    # 로그아웃 버튼
    LOGOUT_BUTTON = 'a:has-text("로그아웃")'