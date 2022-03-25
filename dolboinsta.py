import os
from instapy import InstaPy

browser_executable_path = r'/usr/bin/firefox'

insta_username = os.environ.get('insta_username')
insta_password = os.environ.get('insta_password')

session = InstaPy(username=insta_username,
                  password=insta_password,
                  browser_executable_path=browser_executable_path,
                  headless_browser=True)
session.login()

followings = session.grab_following(insta_username, 1000)
followers = session.grab_followers(insta_username, 1000)

followings_who_dont_follow = set(followings) - set(followers)

for ff in followings_who_dont_follow:
    print(ff)
exit(0)
