#!/usr/bin/env python3
import os

from instapy import InstaPy
from instapy.browser import create_firefox_extension, get_geckodriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def browser_executable_path():
    system_path = r'/usr/bin/firefox'
    app_path = r'/Applications/Firefox.app/Contents/MacOS/firefox'
    if os.path.exists(system_path):
        return system_path
    else:
        if os.path.exists(app_path):
            return app_path
        else:
            raise RuntimeError("Firefox executable not found in {0} and {1}".format(system_path, app_path))


def accept_gdpr(browser):
    browser.get('https://instagram.com/accounts/login')
    WebDriverWait(browser, 60).until(expected_conditions.visibility_of_element_located((By.ID, 'react-root')))
    for element in browser.find_elements(by=By.TAG_NAME, value='button'):
        if element.text.strip().lower() == 'allow essential and optional cookies':
            element.click()
            break


def browser(headless=True):
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument('--headless')
    options.binary = FirefoxBinary(firefox_path=browser_executable_path())
    options.set_preference("permissions.default.image", 2)
    options.set_preference("media.volume_scale", "0.0")
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("useAutomationExtension", False)
    options.set_preference("general.platform.override", "iPhone")

    firefox = webdriver.Firefox(options=options, service=Service(executable_path=get_geckodriver()))
    firefox.set_script_timeout(60)
    firefox.implicitly_wait(60)
    firefox.install_addon(create_firefox_extension(), temporary=True)

    accept_gdpr(firefox)

    return firefox


headless_browser = os.getenv('headless_browser', 'True').lower() in ('true', '1', 't')
insta_username = os.environ.get('insta_username')
insta_password = os.environ.get('insta_password')
if not insta_username or not insta_password:
    raise RuntimeError('Environment variables insta_username and insta_password should be set')

session = InstaPy(username=insta_username,
                  password=insta_password,
                  selenium_local_session=False,
                  headless_browser=headless_browser)
session.browser = browser(headless_browser)
session.login()

followings = session.grab_following(insta_username, 1000)
followers = session.grab_followers(insta_username, 1000)

followings_who_dont_follow = set(followings) - set(followers)

for ff in followings_who_dont_follow:
    print(ff)
session.browser.quit()
