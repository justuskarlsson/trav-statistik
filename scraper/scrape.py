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
import json

from scrape_week import scrape_week
from Column import factors 


ONE_WEEK = timedelta(days=7)

def mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def extend_entries(main, new):
    for key, sequence in new.items():
        main[key] += sequence

def csv_to_dict(path: str):
    factor_ids = {}
    with open(f"{path}/factors.json") as f:
        d = json.load(f)
        for key, val in d.items():
            factor_ids[key] = val
    data = defaultdict(list)
    with open(f"{path}/data.csv") as f:
        column = {i: key.rstrip() for i, key in enumerate(next(f).split(";"))}
        for line in f:
            entries = line.split(";")
            for i, entry in enumerate(entries):
                data[column[i]].append(entry.rstrip())
    return data, factor_ids

def write_to_file(columns, file_name, factors_ids):
    headers = list(columns.keys())
    root = pathlib.Path(__file__).parent.parent.absolute()
    dir_path = f"{root}/data"
    mkdir(dir_path)
    dir_path = f"{dir_path}/{file_name}"
    mkdir(dir_path)

    print("Writing to directory: '{}'".format(dir_path))
    csv_path = f"{dir_path}/data.csv"
    with open(csv_path, "w") as out:
        out.write(";".join(headers) + "\n")
        size = len(columns[headers[0]])
        for i in range(size):
            vals = []
            for header in headers:
                if len(columns[header]) <= i:
                    print(f"Too few for {columns[header]}, {header}, {i}")
                vals.append(columns[header][i])
            out.write(";".join(vals) + "\n")
    with open(f"{dir_path}/factors.json", "w") as f:
        f.write(json.dumps(factors_ids, indent="\t"))


def str_to_date(date_str):
    return datetime(*[int(x) for x in date_str.split("-")])

def date_to_str(date):
    return date.strftime("%Y-%m-%d")

def parse(browser, weeks, start_date_str, extension, args):
    start_date = str_to_date(start_date_str)


    factor_ids = defaultdict(dict)
    columns = defaultdict(list)
    


    for i in range(weeks):
        date = start_date-i*ONE_WEEK
        date_str = date_to_str(date)
        columns_i = scrape_week(browser, date_str, i == 0)
        if len(columns_i) > 0:
            print(f"{i+1}/{weeks} done.")
            extend_entries(columns, columns_i)
        else:
            print(f"Parsing of date {date_str} failed...")

    if extension:
        old_columns, factor_ids = csv_to_dict(extension)
    
    for header, values in columns.items():
        if header not in factors:
            continue
        for i, val in enumerate(values):
            if val not in factor_ids[header]:
                factor_ids[header][val] = len(factor_ids[header])
            columns[header][i] = str(factor_ids[header][val])
    
    if extension:
        extend_entries(old_columns, columns)
        columns = old_columns
        print(len(columns["horseAge"]))

        # So we get the proper name
        weeks += int(extension.split("_")[-1])

    if len(columns) == 0:
        print("Failed to parse any week :(")
    else:
        write_to_file(columns, f"{start_date_str}_{weeks}", factor_ids)

browser = None
try:
    arg_parser = ArgumentParser()

    arg_parser.add_argument("--start-date")
    arg_parser.add_argument("--weeks")
    arg_parser.add_argument("--extension", default="", help="If specified, no need to provide --start-date or --weeks.")
    arg_parser.add_argument("--data-path", default="data")
    
    args = arg_parser.parse_args()

    if args.extension:
        start_date = args.extension.split("_")[0]
        cur_date = str_to_date(start_date)
        # V75 slut kl 19:00
        cur_date += timedelta(hours=19)
        weeks = 0

        while cur_date + ONE_WEEK < datetime.now():
            weeks += 1
            cur_date += ONE_WEEK

        args.weeks = weeks
        args.extension = f"{args.data_path}/{args.extension}"
        args.start_date = date_to_str(cur_date)

    print(args)
    chrome_options = Options()
    browser = webdriver.Chrome(options=chrome_options)

    print("Starting parsing")
    parse(browser, args.weeks, args.start_date, args.extension, args)

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