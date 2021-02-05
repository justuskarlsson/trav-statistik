# UNDER CONSTRUCTION

HTML_PARSER = "html-parser"
TEXT_PARSER = "text-parser"

def get_class_text(root, class_name, element_type="span")
    el = root.findAll(element_type, attrs: {"class": class_name})
    return el[0].text

class Column:
    type = TEXT_PARSER
    def parse(self, text):
        return text

class Integer(Column):
    # Remove blank spaces
    def parse(self, text: str):
        return text.replace(" ", "")

class Decimal(Column):
    def parse(self, text: str):
        text.replace(",", "")

class Text(Column):
    pass

class Percentage(Column):
    pass

class Split(Column):
    def parse(self, text):
        res = text.split(":")
        return res

class HorseSplit(Column):
    type = HTML_PARSER

    columns = [
        ("horseName", "horse-name"),
        ("horseSex", "horse-sex"),
        ("horseAge", "horse-age),
        ("trainerShortName", "trainer-short-name"),
    ]

    def parse(self, cell, data):
        text = cell.text
        i = 0
        while i < len(text) and text[i].isdigit():
            i += 1
        data["horseNumber"].append(text[:i])
        for key, css_class in self.columns:
            val = get_class_text(cell, css_class)
            data[key].append(val)

class 

columns = {
    "horse": HorseSplit(),
    "driver": Text(),
    "betDistribution": Percentage(decimal=True),
    "earnings": Integer(),
    "winPercent": Percentage(),
    "record": Record(),
    "earningsPerStart": Integer(),
    "shoeInfo": ShoeInfo(),
    "cartInfo": Text(),
    "lifeStats": Split(),
    "vOdds": Decimal(),
    "pOdds": Decimal(),
    "postPositionAndDistance": Split(" : "), # Ignore, already have info
    "Tränare": Text(),
    "Plats%": Percentage(),
    "Snittodds": Decimal(),
    "Poäng": Integer(),
    "Hemmabana": Text(),
    "StarterCurrent": Split(),
    "StarterPrev": Split(),
}