from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as parse_html

import time 
from collections import defaultdict
import os

from DataParser import DataParser

URL = "https://www.atg.se/spel/{}/V75"
DATE = "2020-12-19"
url = URL.format(DATE)

chrome_options = Options()

# !! Uncomment below to not open browser window !!
#chrome_options.add_argument("--headless")

browser = webdriver.Chrome(options=chrome_options)
browser.get(url)

def try_until(function, times=100):
    for _ in range(times):
        try:
            function()
            break
        except Exception as e:
            print(e)

def click(id):
    browser.find_element_by_id(id).click()

def click_css(selector, idx=0):
    els = browser.find_elements_by_css_selector(selector)
    els[idx].click()

def click_all_css(selector, root_css):
    root = browser.find_elements_by_css_selector(root_css)[0]
    els = root.find_elements_by_css_selector(selector)
    for el in els:
        el.click()

def accept_cookies():
    click("onetrust-accept-btn-handler")
    # time.sleep(1)

def add_extra_stats():
    click_css("[data-test-id=startlist-customize]")
    # time.sleep(1)
    click_all_css(".css-1tx51pb-Checkbox-styles--icon", ".css-1xikekk-StartlistDisplayOptionsDialog-styles--displayOptionsColumn-StartlistDisplayOptionsDialog-styles--displayOptionsDialogPopular")
    click_all_css(".css-1tx51pb-Checkbox-styles--icon", ".css-13rqg9x-StartlistDisplayOptionsDialog-styles--displayOptionsColumn-StartlistDisplayOptionsDialog-styles--displayOptionsDialogOthers")

    #click_css("[data-test-id=checkbox-earnings]")
    click_css("[data-test-id=save-startlist-options]")


# accept cookies

# get custom fields
try_until(accept_cookies)
try_until(add_extra_stats)

source_code = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
print(f"Length of source code: {len(source_code)}")


html = parse_html(source_code)

races = html.findAll("table", attrs={"class": "game-table"})[1:]

data_parser = DataParser(races)
data_parser.fill_races()

browser.get(url+"/resultat")

source_code = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
html = parse_html(source_code)
results = html.findAll("table", attrs={"class": "game-table"})[1:]
data_parser.fill_results(results)
data_parser.write_to_file(DATE)
while True:
    pass


browser.close()
exit()