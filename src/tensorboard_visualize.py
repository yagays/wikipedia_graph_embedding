import json

import h5py
import torch
from tensorboardX import SummaryWriter

with open("data/jawiki_split_1/dictionary.json") as f:
    dictionary = json.load(f)

with h5py.File("model/jawiki_split_1/embeddings_all_0.v50.h5", "r") as f:
    embeddings = f["embeddings"][:, :]

title2id = {}
with open("data/jawiki-20190901-page.sql.tsv") as f:
    for line in f:
        l = line.strip().split("\t")
        if l[1] != "0":
            continue
        title2id[l[2]] = l[0]
id2title = {v:k for k,v in title2id.items()}
labels = [id2title[i] for i in dictionary["entities"]["all"]]

weights = embeddings[:10000]
labels = labels[:10000]

writer = SummaryWriter()
writer.add_embedding(torch.FloatTensor(weights), metadata=labels)
