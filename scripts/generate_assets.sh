#!/bin/bash
python3 gc_graph_type_generation.py
rm -f ../microbiome/data/gc_graph_types.json
mv gc_graph_types.json ../microbiome/data/
python3 gc_query_type_generation.py
rm -f ../microbiome/data/gc_query_types.json
mv gc_query_types.json ../microbiome/data/
rm -f ../microbiome/data/gc_types.json
python3 gc_type-norm.py -f ../microbiome/data/gc_gc_types.json ../microbiome/data/gc_query_types.json ../microbiome/data/gc_graph_types.json ../microbiome/data/gc_basic_types.json ../microbiome/data/gc_numpy_types.json ../microbiome/data/gc_container_types.json
mv gc_types.json ../microbiome/data/
python3 gc_type-norm.py -f ../microbiome/data/gc_gc_types.json ../microbiome/data/gc_query_types.json ../microbiome/data/gc_graph_types.json ../microbiome/data/gc_basic_types.json ../microbiome/data/gc_numpy_types.json ../microbiome/data/gc_container_types.json
mv gc_codons.json ../microbiome/data/
