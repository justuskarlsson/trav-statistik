
HTML_PARSER = "html-parser"
TEXT_PARSER = "text-parser"

def get_all_classes(root, class_name, element_type="span"):
    return root.findAll(element_type, attrs={"class": class_name})

def get_class_text(root, class_name, element_type="span"):
    if (el := get_all_classes(root, class_name, element_type)):
        return el[0].text
    else:
        return ""

class Column:
    HTML_PARSER = HTML_PARSER
    TEXT_PARSER = TEXT_PARSER
    type = TEXT_PARSER
    def parse(self, text):
        return text

class Text(Column):
    def __init__(self, remove_after = ""):
        self.remove_after = remove_after

    def parse(self, text):
        if self.remove_after:
            idx = text.find(self.remove_after)
            if idx != -1:
                text = text[:idx]
        return text

class Integer(Column):
    def parse(self, text: str):
        return text.replace(" ", "")

class Decimal(Column):
    def parse(self, text: str):
        return text.replace(",", ".")


class Percentage(Column):
    def parse(self, text):
        text = text.replace("%", "")
        text = text.replace(",", ".")
        val = float(text) / 100
        return str(val)

class Record(Column):
    type = HTML_PARSER
    header = "record"

    def parse(self, cell=None, data=None):
        text = cell.text
        suffix = ""
        for i in range(len(text) - 1, -1, -1):
            if text[i].isdigit():
                suffix = text[i] + suffix
        decimal = text[:-len(suffix)].replace(",", ".")
        data[self.header + "-suffix"].append(suffix)
        data[self.header + "-decimal"].append(decimal)


class HorseSplit(Column):
    type = HTML_PARSER

    columns = [
        ("horseName", "horse-name"),
        ("horseSex", "horse-sex"),
        ("horseAge", "horse-age"),
    ]

    @staticmethod
    def get_horse_number(text):
        i = 0
        while i < len(text) and text[i].isdigit():
            i += 1
        return text[:i]

    def parse(self, cell=None, data=None):
        text = cell.text
        horse_number = HorseSplit.get_horse_number(text)
        data["horseNumber"].append(horse_number)
        for key, css_class in self.columns:
            val = get_class_text(cell, css_class)
            data[key].append(val)


class LifeStats(Column):
    type = HTML_PARSER
    header = "lifeStats" 

    def parse(self, cell=None, data=None):
        starts_tag = cell.find("span", attrs={"class": "start-stats__starts"})
        tot_starts = starts_tag.text
        data[self.header+"-tot"].append(tot_starts)
        results = cell.text[len(tot_starts):].split("-")
        for i in range(3):
            data[self.header + f"-{i+1}"].append(results[i])

class ShoeInfo(Column):
    type = HTML_PARSER
    header = "shoeInfo" 

    def parse(self, cell=None, data=None):
        spans = cell.findAll("span")
        val = ["0" for _ in range(4)] # shoe1, change1, shoe2, change2
        for i, span in enumerate(spans):
            self.check_changed(val, span, i)
            self.check_shoe_on(val, span, i)
        data[self.header].append("".join(val))
                
    
    def check_changed(self, val, span, i):
        if self.one_class_includes(span, "changed"):
            val[i*2 + 1] = "1"
        
    def check_shoe_on(self, val, span, i):
        svg = span.find("svg")
        if svg and self.one_class_includes(svg, "shoe-yes"):
            val[i*2] = "1"

    def one_class_includes(self, el, includes):
        classes = el.get("class")
        if classes is None:
            return False
        for css_class in classes:
            if css_class.find(includes) != -1:
                return True
        return False

columns = {
    "horse": HorseSplit(),
    "driver": Text(remove_after="("),
    "betDistribution": Percentage(),
    "earnings": Integer(),
    "winPercent": Percentage(),
    Record.header: Record(),
    "earningsPerStart": Integer(),
    ShoeInfo.header: ShoeInfo(),
    "cartInfo": Text(),
    LifeStats.header: LifeStats(),
    "vOdds": Decimal(),
    "pOdds": Decimal(),
    #"postPositionAndDistance": Split(" : "), # Ignore, already have info
    "Tränare": Text(),
    "Plats%": Percentage(),
    "Snittodds": Decimal(),
    "Poäng": Integer(),
    "Hemmabana": Text(),

    ### Since the starts are always 2021 and 2020, old results won't matter ###
    ### Fortunately we can check the record ourselves in our database ###
    #"StarterCurrent": Split(),
    #"StarterPrev": Split(),
}