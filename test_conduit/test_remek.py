from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

from functions import *
from test_data import *

class TestConduit(object):


    def setup(self):
        browser_options = Options()
        browser_options.headless = True
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
        self.browser.implicitly_wait(10)
        URL = "http://localhost:1667/#/"
        self.browser.get(URL)

    def teardown(self):
        self.browser.quit()


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


    def test_registration_invalid(self):
        registration(self.browser, user_invalid["name"], user_invalid["email"], user_invalid["password"])

        time.sleep(2)

        result_message = self.browser.find_element_by_xpath('//div[@class="swal-title"]')
        result_message2 = self.browser.find_element_by_xpath('//div[@class="swal-text"]')

        assert result_message.text == sys_messages["invalid_reg"]
        assert result_message2.text == sys_messages["invalid_email"]


    def test_sign_in(self):
        sign_in(self.browser, user_valid["email"], user_valid["password"])

        time.sleep(2)

        user_profile = self.browser.find_elements_by_xpath('//a[@class="nav-link"]')[2]

        assert user_profile.text == user_valid['name']


    def test_logout(self):
        TestConduit.test_sign_in(self)
        logout_btn = self.browser.find_element_by_xpath('//a[@active-class="active"]')

        logout_btn.click()

        sign_in_menu = self.browser.find_elements_by_xpath('//a[@href="#/login"]')[0]
        assert sign_in_menu.text == "Sign in"



