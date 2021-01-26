# UNDER CONSTRUCTION


class Column:
    pass

class Integer(Column):
    # Remove blank spaces
    pass

class Text(Column):
    pass

class Percentage(Column):
    pass

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
    "pOdds": 
}