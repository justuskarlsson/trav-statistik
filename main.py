from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as parse_html

import time 
from collections import defaultdict
import os

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

OVERFLOW_LABEL = "css-1dzf2nj-startlistrow-styles--overflowRowLabel"
OVERFLOW_VALUE = "css-1hd5aa-startlistrow-styles--overflowRowValue"

source_code = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
print(f"Length of source code: {len(source_code)}")


html = parse_html(source_code)

races = html.findAll("table", attrs={"class": "game-table"})[1:]
text = ""
columns = defaultdict(list)

for race_idx, race in enumerate(races):
    tds = race.findAll("td")
    for cell in tds:
        if (classes := cell.get("class")) is None:
            continue
        header = classes[0].replace("-col","")
        # Don't add overflow td
        if header:
            text = cell.text
            columns[header].append(text)
    
    olabels = race.findAll(None, attrs={"class": OVERFLOW_LABEL})
    ovalues = race.findAll(None, attrs={"class": OVERFLOW_VALUE})
    assert len(olabels) == len(ovalues)
    for i in range(len(olabels)):
        label = olabels[i].text.replace(":", "")
        value = ovalues[i]

        starts_tag = value.find("span", attrs={"class": "start-stats__starts"})
        if starts_tag:
            starts = starts_tag.text
            columns[label].append(starts)
            results = value.text[len(starts):].split("-")
            for i in range(len(results)):
                columns["{}-{}".format(label, i+1)].append(results[i])
            continue
        
        columns[label].append(value.text)

headers = list(columns.keys())

if not os.path.isdir("data"):
    os.mkdir("data")

file_name = "data/{}.csv".format(DATE)
print("Writing to file: '{}'".format(file_name))

with open(file_name, "w") as out:
    out.write(";".join(headers) + "\n")
    size = len(columns[headers[0]])
    for i in range(size):
        vals = []
        for header in headers:
            vals.append(columns[header][i])
        out.write(";".join(vals) + "\n")

browser.close()
exit()