import os
from selenium import webdriver

current_path = os.path.dirname(os.path.realpath(__file__))
chromedriver_path = os.path.join(current_path, 'chromedriver')


PROXY = '138.68.236.23:3128'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=%s' % PROXY)

chrome = webdriver.Chrome(chromedriver_path, chrome_options=chrome_options)
chrome.get('https://www.whatismyip.com/')
