import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class TestConduit(object):
    def setup(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.implicitly_wait(10)
        URL = "http://localhost:1667/"
        self.browser.get(URL)
        self.browser.maximize_window()

    def test_accept_cookie(self):
        accept_btn = self.browser.find_element_by_xpath(
            '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
        accept_btn.click()
        time.sleep(2)
        decline_btn_list = self.browser.find_elements_by_xpath(
            '//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--decline"]')
        assert not len(decline_btn_list)

browser.quit()
