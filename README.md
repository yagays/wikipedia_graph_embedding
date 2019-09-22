# Pytorch-BigGraphによるWikipedia日本語記事のグラフ埋め込み

## 準備
2019年9月1日時点におけるWikipedia日本語記事のSQLダンプデータをダウンロードします。

```sh
$ wget https://dumps.wikimedia.org/jawiki/20190901/jawiki-20190901-page.sql.gz
$ wget https://dumps.wikimedia.org/jawiki/20190901/jawiki-20190901-pagelinks.sql.gz
```

その後、SQLをパースして記事内のリンク構造を取得します。

```sh
$ python src/parse_page_sql.py
$ python src/convert_relation_tsv.py
```

## 実行する
抽出したグラフ構造に対して、Pytorch-BigGraphを実行します。

```sh
$ torchbiggraph_import_from_tsv --lhs-col=0 --rel-col=1 --rhs-col=2 \
  src/config/jawiki_split_1.py \
  data/jawiki-20190901.tsv

$ torchbiggraph_train src/config/jawiki_split_1.py \
  -p edge_paths=data/jawiki-20190901_partitioned
```

CPUスレッド数にも依存しますが、おおよそ10~12GB程度のメモリが必要です。
