import json
import pickle

import h5py
from pyflann import FLANN
import pandas as pd


with open("data/jawiki_split_1/dictionary.json") as f:
    dictionary = json.load(f)

with h5py.File("model/jawiki_split_1/embeddings_all_0.v50.h5", "r") as f:
    embeddings = f["embeddings"][:, :]


flann = FLANN()
flann.build_index(embeddings)


title2id = {}
with open("data/jawiki-20190901-page.sql.tsv") as f:
    for line in f:
        l = line.strip().split("\t")
        if l[1] != "0":
            continue
        title2id[l[2]] = l[0]
id2title = {v:k for k,v in title2id.items()}


def search(query_title):
    print(f"query: {query_title}")
    query_index = dictionary["entities"]["all"].index(title2id[query_title])
    for rank, result_index in enumerate(flann.nn_index(embeddings[query_index], num_neighbors=10)[0][0]):
        result_title = id2title[dictionary["entities"]["all"][result_index]]
        print(rank, " ", result_title)
