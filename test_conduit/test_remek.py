from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options



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
