from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from argparse import ArgumentParser
from datetime import datetime, timedelta
import os
import subprocess
import time
from threading import Timer 
from collections import defaultdict
import sys
import pathlib
import traceback

from scrape_week import scrape_week
from Column import factors 



def extend_entries(main, new):
    for key, sequence in new.items():
        main[key] += sequence

def write_to_file(columns, file_name):
    headers = list(columns.keys())
    root = pathlib.Path(__file__).parent.parent.absolute()
    dir_path = f"{root}/data"
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    file_path = f"{dir_path}/{file_name}"
    print("Writing to file: '{}'".format(file_path))
    with open(file_path, "w") as out:
        out.write(";".join(headers) + "\n")
        size = len(columns[headers[0]])
        for i in range(size):
            vals = []
            for header in headers:
                vals.append(columns[header][i])
            out.write(";".join(vals) + "\n")







def parse(browser, weeks: int, start_date_str):
    start_date = datetime(*[int(x) for x in start_date_str.split("-")])
    one_week = timedelta(days=7)

    columns = defaultdict(list)
    for i in range(weeks):
        date = start_date-i*one_week
        date_str = date.strftime("%Y-%m-%d")
        columns_i = scrape_week(browser, date_str, i == 0)
        if len(columns_i) > 0:
            print(f"{i+1}/{weeks} done.")
            extend_entries(columns, columns_i)
        else:
            print(f"Parsing of date {date_str} failed...")
    factor_ids = defaultdict(dict)
    for header, values in columns.items():
        if header not in factors:
            continue
        for i, val in enumerate(values):
            if val not in factor_ids[header]:
                factor_ids[header][val] = len(factor_ids[header])
            columns[header][i] = str(factor_ids[header][val])

    if len(columns) == 0:
        print("Failed to parse any week :(")
    else:
        write_to_file(columns, f"{start_date_str}_{weeks}.csv")

browser = None
try:
    arg_parser = ArgumentParser()

    arg_parser.add_argument("--start-date", default="2021-02-20")
    arg_parser.add_argument("--weeks", default=10, type=int)
    
    args = arg_parser.parse_args()

    chrome_options = Options()
    browser = webdriver.Chrome(options=chrome_options)

    print("Starting parsing")
    parse(browser, args.weeks, args.start_date)

except KeyboardInterrupt:
    print("Scraper cancelled by user")
except Exception:
    print("Exception occured:")
    traceback.print_exc()

finally:
    if browser is not None:
        print("Cleaning up")
        browser.close()
        exit()