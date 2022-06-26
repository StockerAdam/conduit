from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from functions import *
from test_data import *


class TestConduit(object):

    # •  •  • Adatok lementése felületről •
    def setup(self):
        browser_options = Options()
        browser_options.headless = True
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
        self.browser.implicitly_wait(10)
        URL = "http://localhost:1667/#/"
        self.browser.get(URL)

    def teardown(self):
        self.browser.quit()

    # 1.Adatkezelési nyilatkozat használata
    def test_cookie(self):
        cookie_bar = WebDriverWait(self.browser, 7).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class = "cookie__bar__buttons"]')))
        assert cookie_bar.is_displayed()

        accept_btn_list_before_click = self.browser.find_elements_by_xpath(
            '//button[@class ="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        print(len(accept_btn_list_before_click))

        cookie_btn_ok = WebDriverWait(self.browser, 7).until(EC.presence_of_element_located(
            (By.XPATH, '//button[@class ="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')))
        cookie_btn_ok.click()

        time.sleep(5)

        accept_btn_list_after_click = self.browser.find_elements_by_xpath(
            '//button[@class ="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')

        print(len(accept_btn_list_after_click))

        assert not len(accept_btn_list_after_click)

    # 2.a Regisztráció helytelen adatokkal
    def test_registration_invalid(self):
        registration(self.browser, user_invalid["name"], user_invalid["email"], user_invalid["password"])

        time.sleep(2)

        result_message = self.browser.find_element_by_xpath('//div[@class="swal-title"]')
        result_message2 = self.browser.find_element_by_xpath('//div[@class="swal-text"]')

        assert result_message.text == sys_messages["invalid_reg"]
        assert result_message2.text == sys_messages["invalid_email"]

    # 2.b Regisztráció megfelelő (valid) adatokkal
    def test_registration_valid(self):
        registration(self.browser, user_valid["name"], user_valid["email"], user_valid["password"])

        time.sleep(2)

    # 3. Bejelentkezés valid, regisztrált adatokkal
    def test_sign_in(self):
        sign_in(self.browser, user_valid["email"], user_valid["password"])

        time.sleep(2)

        user_profile = self.browser.find_elements_by_xpath('//a[@class="nav-link"]')[2]

        assert user_profile.text == user_valid['name']

    # 4. Adatok listázása
    def test_list_popular_tags(self):
        popular_tags = self.browser.find_elements_by_xpath('//a[@class="tag-pill tag-default"]')

        list_of_pop_tags = []
        for i, k in enumerate(popular_tags):
            list_of_pop_tags.append(f'{i + 1}. popular tag: {k.text}')
        assert len(list_of_pop_tags) == len(popular_tags)

    # 5. Több oldalas lista bejárása
    def test_page_navigation(self):
        TestConduit.test_sign_in(self)
        pages = self.browser.find_elements_by_xpath('//a[@class="page-link"]')
        for page in pages:
            page.click()
            time.sleep(2)
            current_page = self.browser.find_element_by_xpath('//li[@class="page-item active"]')
            assert page.text == current_page.text

    # 6. Új adat (cikk) bevitel
    def test_adding_new_input(self):
        TestConduit.test_sign_in(self)
        create_new_article(self.browser, new_article['title'], new_article['about'], new_article['body'], new_article['tag'])

        time.sleep(2)

        article_body = self.browser.find_element_by_xpath('//p')
        assert article_body.text == new_article['body']

    # 7. Ismételt és sorozatos adatbevitel adatforrásból
    def test_import_articles(self):
        TestConduit.test_sign_in(self)
        with open('test_conduit/articles.csv', 'r') as file:
            csv_reader = csv.reader(file, delimiter=':')
            for row in csv_reader:
                create_new_article(self.browser, row[0], row[1], row[2], row[3])
                time.sleep(2)
                article_body = self.browser.find_element_by_xpath('//p')
                assert article_body.text == row[2]

    # 8. Adat vagy adatok törlése (MÓDOSÍTJA A USERNAMET!!!!)
    def test_delete_article(self):
        TestConduit.test_sign_in(self)
        time.sleep(1)

        comments_list_before = self.browser.find_elements_by_xpath('//div[@class="card"]')

        author = self.browser.find_element_by_xpath(
            '//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div/div/div[1]/div/div/a').text

        change_name(self.browser, author)

        assert self.browser.find_element_by_xpath('//div[@class="swal-title"]').text == 'Update successful!'

        time.sleep(1)

        home = self.browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[1]/a')
        home.click()

        time.sleep(1)

        first_article = self.browser.find_element_by_xpath(
            '//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div/div/div[1]/a/h1')
        first_article.click()

        time.sleep(1)

        delete_btn = self.browser.find_element_by_xpath('//button[@class="btn btn-outline-danger btn-sm"]')
        delete_btn.click()

        comments_list_after = self.browser.find_elements_by_xpath('//div[@class="card"]')

        assert len(comments_list_after) == len(comments_list_before)

    # 9. Meglévő adat módosítás
    def test_name_change(self):
        TestConduit.test_sign_in(self)
        change_name(self.browser, "Entertester")

        assert self.browser.find_element_by_xpath('//div[@class="swal-title"]').text == 'Update successful!'

    #Kijelentkezés
    def test_logout(self):
        TestConduit.test_sign_in(self)
        logout_btn = self.browser.find_element_by_xpath('//a[@active-class="active"]')

        logout_btn.click()

        sign_in_menu = self.browser.find_elements_by_xpath('//a[@href="#/login"]')[0]
        assert sign_in_menu.text == "Sign in"
