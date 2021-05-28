import sys
import json

path = sys.argv[1]
out = f"{path}/horseNames.csv"



with open(f"{path}/factors.json") as f:
    data = json.load(f)
    names = list(data["horseName"].keys())

with open(out, "w") as f:
    f.write("\n".join(names))
