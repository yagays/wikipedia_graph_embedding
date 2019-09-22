
title2id = {}
with open("data/jawiki-20190901-page.sql.tsv") as f:
    for line in f:
        l = line.strip().split("\t")
        if l[1] != "0":
            continue
        title2id[l[2]] = l[0]
page_id_set = set(title2id.values())


with open("data/jawiki-20190901-pagelinks.sql.tsv") as f:
    with open("data/jawiki-20190901.tsv", "w") as ff:
        for line in f:
            l = line.strip().split("\t")

            # page.sqlにpagelinksのtitleが含まれていなかった場合
            if l[2] not in title2id:
                print(l[2])
                continue
            # pagelinks内のpage_idがpage.sqlに含まれていなかった場合
            if l[0] not in page_id_set:
                print(l[0])
                continue

            ff.write("\t".join([l[0], "has_link_to", title2id[l[2]]]) + "\n")
