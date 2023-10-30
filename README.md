# ete-data

Data files to use with the [ETE Toolkit](https://github.com/etetoolkit/ete/).

They include data such as big example files and GTDB taxonomy data.


## How to create the gtdb-dump files

To create the `gtdbdump.tar.gz` files in
[gtdb_taxonomy](gtdb_taxonomy), we first get the archea and bacteria
data from https://data.gtdb.ecogenomic.org/releases/latest/ (for
example,
[ar53_taxonomy](https://data.gtdb.ecogenomic.org/releases/latest/ar53_taxonomy.tsv.gz)
and
[bac120_taxonomy](https://data.gtdb.ecogenomic.org/releases/latest/bac120_taxonomy.tsv.gz).

Then, we use Nick Youngblut's
[gtdb_to_taxdump](https://github.com/nick-youngblut/gtdb_to_taxdump)
(which can also be found in [tools -> third
party](https://gtdb.ecogenomic.org/tools)) to convert GTDB taxonomy to
NCBI taxdump format. To do it, we run:

```sh
gtdb_to_taxdump.py ar53_taxonomy.tsv.gz bac120_taxonomy.tsv.gz
```

and then just put the 4 resulting `.dpm` files into a tar.gz:

```sh
tar -cfz gtdb_latest_dump.tar.gz *.dmp
```
