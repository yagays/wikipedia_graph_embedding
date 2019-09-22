echo "Processing torchbiggraph_import_from_tsv..."
torchbiggraph_import_from_tsv --lhs-col=0 --rel-col=1 --rhs-col=2 \
  src/config/jawiki_split_1.py \
  data/jawiki-20190901.tsv

echo "Processing torchbiggraph_train..."
torchbiggraph_train src/config/jawiki_split_1.py \
  -p edge_paths=data/jawiki-20190901_partitioned
