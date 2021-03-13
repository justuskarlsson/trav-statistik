from Column import columns, Column, HorseSplit, get_class_text
from collections import defaultdict
import os
import traceback
import pathlib

OVERFLOW_LABEL = "css-1dzf2nj-startlistrow-styles--overflowRowLabel"
OVERFLOW_VALUE = "css-1hd5aa-startlistrow-styles--overflowRowValue"

class DataParser:
    def __init__(self):
        self.columns = defaultdict(list)

    def parse_week(self, html, results_html, date: str):
        self.cur_date = date
        races = html.findAll("table", attrs={"class": "game-table"})[1:]
        self.races = races
        self.fill_races()

        results = results_html.findAll("table", attrs={"class": "game-table"})[1:]
        self.fill_results(results)
    
    def predict(self, html, date: str):
        self.cur_date = date
        races2 = html.findAll("table", attrs={"class": "game-table"})
        races = races2
        self.races = races
        self.fill_races()
        self.columns["raceIdx"] = [ str(race_idx + 1) for race_idx in self.columns["raceIdx"] ]

    def parse_cell(self, header, cell):
        try:
            if header in columns:
                parser: Column  = columns[header]
                if parser.type == Column.TEXT_PARSER:
                    val = parser.parse(cell.text)
                    self.columns[header].append(val)
                elif parser.type == Column.HTML_PARSER:
                    parser.parse(cell, self.columns)
        except Exception:
            print(f"Error for header: '{header}':")
            traceback.print_exc()
    
    def fill_races(self):
        horse_counter = 0
        for race_idx, race in enumerate(self.races):
            tds = race.findAll("td")
            for cell in tds:
                if (classes := cell.get("class")) is None:
                    continue
                header = classes[0].replace("-col","")
                self.parse_cell(header, cell)
            
            olabels = race.findAll(None, attrs={"class": OVERFLOW_LABEL})
            ovalues = race.findAll(None, attrs={"class": OVERFLOW_VALUE})
            assert len(olabels) == len(ovalues)
            for i in range(len(olabels)):
                header = olabels[i].text.replace(":", "")
                cell = ovalues[i]
                self.parse_cell(header, cell)
            while horse_counter < len(self.columns["horseNumber"]):
                self.columns["raceIdx"].append(race_idx)
                horse_counter += 1
            
                

    def fill_results(self, results):
        race_placements = []
        for race in results:
            placements = ["d" for _ in range(20)]
            rows = race.findAll("tr")
            for row in rows[1:]:
                horse_text = get_class_text(row, "horse-col", "td")
                idx = HorseSplit.get_horse_number(horse_text)
                idx = int(idx)
                placement = get_class_text(row, "place-col","td")
                placement = '99' if placement == '0' else placement
                placements[idx] = placement
            race_placements.append(placements)
        for i in range(len(self.columns["horseNumber"])):
            horse_number = int(self.columns["horseNumber"][i])
            race_idx = self.columns["raceIdx"][i]
            placement = race_placements[race_idx][horse_number]
            self.columns["result"].append(placement)
            won = placement.isdigit() and int(placement) == 1
            self.columns["won"].append(str(int(won)))
            p_value = won * float(self.columns["vOdds"][i])
            self.columns["pValue"].append(str(p_value))
            self.columns["plats"].append("1" if placement.isdigit() and  int(placement) <= 3 else "0")

        for i in range(len(self.columns["raceIdx"])):
            self.columns["raceIdx"][i] = str(self.columns["raceIdx"][i] + 1)
            

