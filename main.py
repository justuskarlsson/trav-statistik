from argparse import ArgumentParser
from datetime import datetime, timedelta
import os
import subprocess
import time
from threading import Timer 
import sys

arg_parser = ArgumentParser()
arg_parser.add_argument("--start-date", default="2021-02-20")
arg_parser.add_argument("--weeks", default=10, type=int)

args = arg_parser.parse_args()

start_date = datetime(*[int(x) for x in args.start_date.split("-")])
one_week = timedelta(days=7)

weeks = args.weeks

class Script:
    MAX_CONCURRENT = 1
    TIMEOUT = 15
    cur_scripts = {}
    script_counter = 0
    dates = []
    num_done = 0
    max_tries = 3

    def __init__(self, script_args, date):
        self.date = date
        self.script_args = script_args
        self.tries = 0
        self.start_script()
        
    def start_script(self):
        self.key = Script.script_counter
        Script.script_counter += 1
        self.instance = subprocess.Popen(self.script_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL)
        timeout = Timer(Script.TIMEOUT, lambda: self.instance.kill())
        timeout.start()
        self.tries += 1
        Script.cur_scripts[self.key] = self

    def wait_and_kill(self):
        
        self.instance.wait()
        ret = self.instance.returncode
        self.instance.kill()
        Script.cur_scripts.pop(self.key)

        if ret != 0:
            print(f"wait and kill id({self.date}): {self.tries}/{Script.max_tries}")
            if self.tries >= Script.max_tries:
                print(f"Too many retries for args: {self.script_args}")
                return
            self.start_script()
        else:
            Script.num_done += 1
            Script.dates.append(self.date)
            print(f"{Script.num_done}/{weeks} scripts done")

    @staticmethod
    def check_max_concurrent(always_wait=False):
        if always_wait or len(Script.cur_scripts) >= Script.MAX_CONCURRENT:
            scripts = list(Script.cur_scripts.values())
            for script in scripts:
                script.wait_and_kill()
        

try:
    
    for i in range(weeks):
        date = start_date-i*one_week
        date_str = date.strftime("%Y-%m-%d")
        Script.check_max_concurrent()
        cmd = ["python", "scrape_week.py", "--date", date_str]
        Script(cmd, date_str)
    while Script.cur_scripts:
        Script.check_max_concurrent(always_wait=True)
    out_lines = []
    for date in Script.dates:
        file_path = f"data/{date}.csv"
        with open(file_path) as file:
            lines = file.readlines()
            if not out_lines:
                out_lines.append(lines[0])
            out_lines += lines[1:]
            print(len(out_lines))
        os.unlink(file_path)
    if len(Script.dates) == 0:
        print("Every week failed :(")
        sys.exit(1)
    out_file_path = f"data/{Script.dates[0]}-{weeks}.csv"
    with open(out_file_path, "w") as out:
        out.write("".join(out_lines))
    print(f"Wrote combined output for weeks to '{out_file_path}'")
except KeyboardInterrupt:
    print("Killing scripts")
    for script in Script.cur_scripts.values():
        script.instance.kill()
    print("Killed all scripts")
