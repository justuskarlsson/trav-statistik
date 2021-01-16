from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time 
from collections import defaultdict
URL = "https://www.atg.se/spel/{}/V75"
DATE = "2020-12-19"
url = URL.format(DATE)

chrome_options = Options()

#chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=chrome_options)
browser.get(url)

def try_until(function, times=100):
    for i in range(times):
        try:
            function()
            break
        except Exception as e:
            print(e)

def click(id):
    browser.find_element_by_id(id).click()

def click_css(selector, idx=0):
    els = browser.find_elements_by_css_selector(selector)
    print("Elements:", els)
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
out = open("data/{}.csv".format(DATE), "w")

source_code = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
print(f"Length of source code: {len(source_code)}")
from bs4 import BeautifulSoup as parse_html

html = parse_html(source_code)

races = html.findAll("table", attrs={"class": "game-table"})[1:]
text = ""
columns = defaultdict(list)

for race_idx, race in enumerate(races):
    tds = race.findAll("td")
    for cell in tds:
        print(type(cell))
        print(cell.get("class"))
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
        value = ovalues[i].text
        columns[label].append(value)

headers = list(columns.keys())
print("writing to file")
out.write(";".join(headers) + "\n")
size = len(columns[headers[0]])
for i in range(size):
    vals = []
    for header in headers:
        vals.append(columns[header][i])
    out.write(";".join(vals) + "\n")

browser.close()
exit()