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

