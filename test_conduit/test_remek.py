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
    def setup(self):
        browser_options = Options()
        browser_options.headless = True
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
        self.browser.implicitly_wait(10)
        URL = "http://localhost:1667/#/"
        self.browser.get(URL)

    def teardown(self):
        self.browser.quit()


    # 1.Adatkezelési nyilatkozat használata: Az adatkezelési nyilatkozatot elfogadjuk, majd ellenőrizzük,
    # hogy ez megtörtént-e (eltűnt-e az erről szóló értesítés).
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


    # 2.a Regisztráció helytelen adatokkal: A regisztráció során minden invalid értékeket használva, ellenőrizzük,
    # hogy megkapjuk-e a sikerelen regisztrációról szóló üzenetet.
    def test_registration_invalid(self):
        registration(self.browser, user_invalid["name"], user_invalid["email"], user_invalid["password"])

        time.sleep(2)

        result_message = self.browser.find_element_by_xpath('//div[@class="swal-title"]')
        result_message2 = self.browser.find_element_by_xpath('//div[@class="swal-text"]')

        assert result_message.text == sys_messages["invalid_reg"]
        assert result_message2.text == sys_messages["invalid_email"]


    # 2.b Regisztráció megfelelő (valid) adatokkal: Regisztráció valid adatokkal. Ellenőrzés itt külön nincs,
    # mert a folyamat csak egyszer végrehajtható, így ez kiegészítése a regisztrációról szóló esetnek.
    def test_registration_valid(self):
        registration(self.browser, user_valid["name"], user_valid["email"], user_valid["password"])

        time.sleep(2)


    # 3. Bejelentkezés valid, regisztrált adatokkal: A 2.b pontban regisztrált adatokkal való belépés után ellenőrizzük,
    # hogy a profil név a kezdőoldalon megegyezik-e a regisztrál névvel.
    def test_sign_in(self):
        sign_in(self.browser, user_valid["email"], user_valid["password"])

        time.sleep(2)

        user_profile = self.browser.find_elements_by_xpath('//a[@class="nav-link"]')[2]

        assert user_profile.text == user_valid['name']


    # 4. Adatok listázása: kilistázzuk az oldalon található népszerű (popular) tag-eket. Ellenőrizzük,
    # hogy az oldalon található tagek száma megegyezik-e az általam készített lista elemszámával.
    def test_list_popular_tags(self):
        popular_tags = self.browser.find_elements_by_xpath('//a[@class="tag-pill tag-default"]')

        list_of_pop_tags = []
        for i, k in enumerate(popular_tags):
            list_of_pop_tags.append(f'{i + 1}. popular tag: {k.text}')
        assert len(list_of_pop_tags) == len(popular_tags)


    # 5. Adatok lementése felületről: A népszerű (popular) tag-eket kigyűjtjük és lementjük egy listába sorszámozva.
    # A kigyűtő ciklus lefutásainak számát összehasonlítjuk az oldalon található tagek számával.
    def test_export_data(self):
        with open("pop_tag_list.txt", "w", encoding="UTF-8", newline='') as file:
            popular_tags = self.browser.find_elements_by_xpath(
                '//div[@class="sidebar"]//a[@class="tag-pill tag-default"]')
            counter = 0
            for i, k in enumerate(popular_tags):
                file.write(f'{i + 1}.{k.text}' "\n")
                counter += 1
        assert counter == len(popular_tags)


    # 6. Több oldalas lista bejárása: Az alsó oldalnavigációs menűben lapozva ellenőrizzük,
    # hogy az oldalszám megegyező-e.
    def test_page_navigation(self):
        TestConduit.test_sign_in(self)
        pages = self.browser.find_elements_by_xpath('//a[@class="page-link"]')
        for page in pages:
            page.click()
            time.sleep(2)
            current_page = self.browser.find_element_by_xpath('//li[@class="page-item active"]')
            assert page.text == current_page.text


    # 7. Új adat (cikk) bevitel: Egy előre meghatározott tartalmú cikk (article) felvitele. Ellenőrizzük,
    # hogy cikk fő tartalma (body) a létrehozást követően, megegyezik-e az általunk bevitt tartalommal.
    def test_adding_new_input(self):
        TestConduit.test_sign_in(self)
        create_new_article(self.browser, new_article['title'], new_article['about'], new_article['body'], new_article['tag'])

        time.sleep(2)

        article_body = self.browser.find_element_by_xpath('//p')
        assert article_body.text == new_article['body']


    # 8. Ismételt és sorozatos adatbevitel adatforrásból. Egy csv kiterjesztésű file-ból több cikket felviszünk az oldalra.
    # Minden egyes cikk felvitele után ellenőrizzük hogy cikk fő tartalma (body) a létrehozást követően, megegyezik-e az általunk bevitt tartalommal.
    def test_import_articles(self):
        TestConduit.test_sign_in(self)
        with open('test_conduit/articles.csv', 'r') as file:
            csv_reader = csv.reader(file, delimiter=':')
            for row in csv_reader:
                create_new_article(self.browser, row[0], row[1], row[2], row[3])
                time.sleep(2)
                article_body = self.browser.find_element_by_xpath('//p')
                assert article_body.text == row[2]


    # 9. Adat vagy adatok törlése: Az oldalon található első cikk szerzőjének nevére megváltoztatva a profil nevünket,
    # jogot kapunk a felhasznált szerző összes cikkjének a módosításához, törléséhez. Töröljük az első cikket.
    # Két elleőrzést végzünk. Az egyik az, hogy a név változás megtörtént-e, a másik pedig, hogy törlődött-e a cikk (cikkszám alapján).
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

        change_name(self.browser, "Entertester")


    # 10. Meglévő adat módosítás: Megváltoztatjuk a profil nevünket, majd ellenőrizzük az erről kapott üzenetet.
    def test_name_change(self):
        TestConduit.test_sign_in(self)
        change_name(self.browser, "Entertester")

        assert self.browser.find_element_by_xpath('//div[@class="swal-title"]').text == 'Update successful!'


    # 11. Kijelentkezés: Kijelentkezünk, majd ellenőrizzük, hogy megjelent-e a "Sign in" (bejelentkezés) menüpont,
    # azaz ki vagyunk-e jelentkezve.
    def test_logout(self):
        TestConduit.test_sign_in(self)
        logout_btn = self.browser.find_element_by_xpath('//a[@active-class="active"]')

        logout_btn.click()

        sign_in_menu = self.browser.find_elements_by_xpath('//a[@href="#/login"]')[0]
        assert sign_in_menu.text == "Sign in"
