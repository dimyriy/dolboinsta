import os

from instapy import InstaPy
from instapy.browser import create_firefox_extension, get_geckodriver
from selenium import webdriver


def browser_executable_path():
    return r'/usr/bin/firefox'


def browser():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.binary_location = browser_executable_path()
    profile = webdriver.FirefoxProfile()
    profile.set_preference("permissions.default.image", 2)
    profile.set_preference("media.volume_scale", "0.0")
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference("useAutomationExtension", False)
    profile.set_preference("general.platform.override", "iPhone")
    driver_path = get_geckodriver()
    firefox = webdriver.Firefox(firefox_profile=profile, options=options, executable_path=driver_path)
    firefox.install_addon(create_firefox_extension(), temporary=True)
    return firefox


insta_username = os.environ.get('insta_username')
insta_password = os.environ.get('insta_password')

session = InstaPy(username=insta_username,
                  password=insta_password,
                  selenium_local_session=False,
                  headless_browser=True)
session.browser = browser()
session.login()

followings = session.grab_following(insta_username, 1000)
followers = session.grab_followers(insta_username, 1000)

followings_who_dont_follow = set(followings) - set(followers)

for ff in followings_who_dont_follow:
    print(ff)
session.browser.quit()
