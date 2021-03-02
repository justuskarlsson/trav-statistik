from bs4 import BeautifulSoup as parse_html

import time 
import sys
from collections import defaultdict
import os
from argparse import ArgumentParser

from DataParser import DataParser



def scrape_week(browser, date, first: bool) -> defaultdict: 

    URL = "https://www.atg.se/spel/{}/V75"
    url = URL.format(date)
    data_parser = DataParser()
    
    browser.get(url)

    def try_until(function, max_time=1.0) -> bool:
        exception = None
        iterations = 10
        for i in range(iterations):
            try:
                function()
                return True
            except Exception as e:
                exception = e
                if i < iterations - 1:
                    time.sleep(max_time/iterations)

        print(f"'try_until', too many failures: {exception}")
        return False
        

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
    if first:
        success = try_until(accept_cookies)
        success = success and try_until(add_extra_stats)
        if not success:
            return defaultdict(list)

    source_code = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
    html = parse_html(source_code)
    
    browser.get(url+"/resultat")
    source_code = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
    results_html = parse_html(source_code)

    
    data_parser.parse_week(html, results_html, date)

    return data_parser.columns