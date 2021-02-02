# UNDER CONSTRUCTION

class Column:
    def parse(self, text):
        return text

class Integer(Column):
    # Remove blank spaces
    def parse(self, text: str):
        return text.replace(" ", "")

class Text(Column):
    pass

class Percentage(Column):
    pass

class Split(Column):
    def parse(self, text):
        res = text.split(":")
        return res


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
    "postPositionAndDistance": Split(" : "),
    "Tränare": Text(),
    "Plats%": Percentage(),
    "Snittodds": Decimal(),
    "Poäng": Integer(),
    "Hemmabana": Text(),
    "StarterCurrent": Split(),
    "StarterPrev": Split(),
}