import time


def registration(browser, username, email, password):
    sign_up_btn = browser.find_element_by_xpath('//a[@href="#/register"]')
    sign_up_btn.click()
    username_input = browser.find_element_by_xpath('//input[@placeholder="Username"]')
    email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
    password_input = browser.find_element_by_xpath('//input[@placeholder="Password"]')
    sign_up_send_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    username_input.send_keys(username)
    email_input.send_keys(email)
    password_input.send_keys(password)
    sign_up_send_btn.click()

def sign_in(browser, email, password):
    sign_in_menu = browser.find_elements_by_xpath('//a[@href="#/login"]')[0]
    sign_in_menu.click()
    email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
    email_input.send_keys(email)
    password_input = browser.find_element_by_xpath('//input[@placeholder="Password"]')
    password_input.send_keys(password)
    sign_in_btn = browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]')
    sign_in_btn.click()

def create_new_article(browser, title, about, body, tag):
    post_article_btn = browser.find_element_by_xpath('//a[@href="#/editor"]')
    post_article_btn.click()

    time.sleep(2)

    article_title = browser.find_element_by_xpath('//input[@placeholder ="Article Title"]')
    article_title.send_keys(title)

    article_about = browser.find_element_by_xpath('//input[contains(@placeholder, "this article about?")]')
    article_about.send_keys(about)

    article_body = browser.find_element_by_xpath(
        '//textarea[@placeholder ="Write your article (in markdown)"]')
    article_body.send_keys(body)

    article_tag = browser.find_element_by_xpath('//input[@placeholder ="Enter tags"]')
    article_tag.send_keys(tag)

    create_article_btn = browser.find_element_by_xpath('//button[@type="submit"]')
    create_article_btn.click()