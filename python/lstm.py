import torch
import torch.nn as nn
import torch.optim as optim
from config import Config



class Encoder(nn.Module):
    def __init__(self, factors: dict):

        super().__init__()

        self.embedding = dict()
        for factor_key, factor_val in factors.items():
            input_dim = len(factor_val)
            self.embedding[factor_key] = nn.Embedding(input_dim, input_dim//4)

        self.lstm = nn.LSTM(Config.embedding_dim, Config.hidden_dim, Config.n_layers_lstm, batch_first=True)

    def forward(self, src: dict, factors: dict):
        n = None # Will be set
        for column_key, column in src.items():
            n = len(src[column_key])
            if column_key in factors:
                print(repr(column_key))
                print(self.embedding)
                t_val = torch.tensor(column, dtype=torch.long)
                column = self.embedding[column_key](t_val)
            else:
                column = torch.tensor(column)
            src[column_key] = column
        src = [ [ src[key][i] for key in src ] for i in range(n) ]
        src = torch.tensor(src)
        outputs, (hidden, cell) = self.lstm(src)
        return hidden, cell


if __name__ == "__main__":
    import json
    dir = "data/2021-03-20_502/"
    factors = json.load(open(dir + "factors.json"))
    with open(dir + "data.csv") as f:
        headers = [header for header in next(f).split(";")]
        data = { header: [] for header in headers }
        for line in f:
            for i, val in enumerate(line.split(";")):
                entry = None
                try:
                    entry = float(val)
                except Exception:
                    entry = 999.9
                data[headers[i]].append(entry)
    # print([len(data[key]) for key in data])
    enc = Encoder(factors)
    res = enc.forward(data, factors)
    print(res)