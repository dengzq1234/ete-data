# ete-data

Data files to use with the [ETE Toolkit](https://github.com/etetoolkit/ete/).

They include data such as big example files and GTDB taxonomy data.

## How to use update GTDB database for ete4 
In the documentation of ETE Toolkit (https://etetoolkit.github.io/ete/tutorial/tutorial_taxonomy.html#id3), we introduce how to set up he local copies of GTDB taxonomy database in your own terminal. And in the folder https://github.com/etetoolkit/ete-data/tree/main/gtdb_taxonomy of this repo, we prepared the GTDB taxonomy data in different historical releases. Here we showcases how to use it to update in ete4.

### Download specific release of GTDB database 
Here we use release 207 as an example. Please make sure to download the raw dump file from each release folder such as https://github.com/etetoolkit/ete-data/raw/main/gtdb_taxonomy/gtdb207/gtdb207dump.tar.gz instead of https://github.com/etetoolkit/ete-data/blob/main/gtdb_taxonomy/gtdb207/gtdb207dump.tar.gz

```
wget https://github.com/etetoolkit/ete-data/raw/main/gtdb_taxonomy/gtdb207/gtdb207dump.tar.gz
```

### Update the downloaded specific release of GTDB database in ete4 
Then import ete4 in python console or script to update the database 
```
from ete4 import GTDBTaxa
gtdb = GTDBTaxa()
gtdb.update_taxonomy_database("./gtdb207dump.tar.gz") 
```

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
