import csv
import gzip
import codecs
import argparse

import sqlparse
from tqdm import tqdm


def is_insert_line(line):
    return line.startswith("INSERT INTO") or False


def parse_with_sql(line):
    print(f"parse_with_sql: {line[:100]}")
    output = []
    tokens = sqlparse.parse(line)[0].tokens
    for token in tokens:
        if str(token).startswith("("):
            parsed_value = csv.reader([str(token).strip("()")],
                                      delimiter=',',
                                      doublequote=False,
                                      escapechar='\\',
                                      quotechar="'",
                                      strict=True)
            for row in parsed_value:
                output.append("\t".join(row) + "\n")
    return output

def parse_with_split(line):
    output = []
    values = line.partition("` VALUES ")[2]
    for value in values.split("),("):
        v = value.strip("();")
        parsed_value = csv.reader([v], delimiter=',', doublequote=False, escapechar='\\', quotechar="'", strict=True)
        for row in parsed_value:
            output.append("\t".join(row) + "\n")
    return output


def parse_line(line):
    try:
        return parse_with_split(line)
    except:
        return parse_with_sql(line)


with codecs.open("data/jawiki-20190901-page.sql", "r", "utf-8", "ignore") as fin:
    with open("data/jawiki-20190901-page.sql.tsv", "w") as fout:
        for l in tqdm(fin,total=456):
            line = l.strip()
            if is_insert_line(line):
                fout.write("".join(parse_line(line)))

with codecs.open("data/jawiki-20190901-pagelinks.sql", "r", "utf-8", "ignore") as fin:
    with open("data/jawiki-20190901-pagelinks.sql.tsv", "w") as fout:
        for l in tqdm(fin,total=4853):
            line = l.strip()
            if is_insert_line(line):
                fout.write("".join(parse_line(line)))
