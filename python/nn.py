import torch
import torch.nn as nn
import torch.optim as optim
from config import Config
import numpy as np




class Encoder(nn.Module):
    def __init__(self, factors: dict):

        super().__init__()

        self.embedding = dict()
        for factor_key, factor_val in factors.items():
            input_dim = len(factor_val)
            self.embedding[factor_key] = nn.Embedding(input_dim, 8)

        self.lstm = nn.LSTM(Config.embedding_dim, Config.hidden_dim, Config.n_layers_lstm, batch_first=True)

    def forward(self, src: dict, factors: dict):

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
    

    enc = Encoder(factors)
    n = len(data[list(data)[0]])

    for column_key, column in data.items():
        if column_key in factors:
            column = torch.tensor(column)
            column = enc.embedding[column_key](column)
        data[column_key] = torch.Tensor(column)
    d = [ [ data[key][i] for key in data] for i in range(n)]
    print("KUK")
    data = torch.tensor(d)
    print("KUK")

    sample = np.random.choice(data, 64)
    enc.forward(sample)