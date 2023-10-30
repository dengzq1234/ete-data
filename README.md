# ete-data

Data files to use with the [ETE Toolkit](https://github.com/etetoolkit/ete/).

They include data such as big example files and GTDB taxonomy data.


## How to create the gtdb-dump files

The data in the `gtdb*dump.tar.gz` files in the
[gtdb_taxonomy](gtdb_taxonomy) directory come from the [Genome
Taxonomy Database](https://gtdb.ecogenomic.org/).

To create them, we first get the archea and bacteria taxonomies from
[their releases](https://data.gtdb.ecogenomic.org/releases/) (for
example, for the [latest
release](https://data.gtdb.ecogenomic.org/releases/latest),
[ar53_taxonomy](https://data.gtdb.ecogenomic.org/releases/latest/ar53_taxonomy.tsv.gz)
and
[bac120_taxonomy](https://data.gtdb.ecogenomic.org/releases/latest/bac120_taxonomy.tsv.gz)).

Then, we use Nick Youngblut's
[gtdb_to_taxdump](https://github.com/nick-youngblut/gtdb_to_taxdump)
(which can also be found in [tools -> third
party](https://gtdb.ecogenomic.org/tools)) to convert GTDB taxonomy to
NCBI taxdump format. To do it, we run:

```sh
gtdb_to_taxdump.py ar53_taxonomy.tsv.gz bac120_taxonomy.tsv.gz
```

and then we just put the 4 resulting `.dmp` files into a tar.gz:

```sh
tar -cfz gtdb_latest_dump.tar.gz *.dmp
```
