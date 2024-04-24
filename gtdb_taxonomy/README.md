This folder contains the GTDB taxonomy data in different historical
releases, ready for use with Ete (see also [its
documentation](https://etetoolkit.github.io/ete/tutorial/tutorial_taxonomy.html#id3)
for more details).


## How to create them

To create the `gtdb*dump.tar.gz` files, we first get the archea and
bacteria taxonomies from [their releases](https://data.gtdb.ecogenomic.org/releases/)
(for example, for the [latest release](https://data.gtdb.ecogenomic.org/releases/latest),
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
tar -czf gtdb_latest_dump.tar.gz *.dmp
```


## How to use GTDB databases in Ete4

Let's download release 207 as an example:

```
wget https://github.com/etetoolkit/ete-data/raw/main/gtdb_taxonomy/gtdb207/gtdb207dump.tar.gz
```

(Note that we download the raw dump file, `.../ete-data/raw/main/...`,
and not `.../ete-data/blob/main/...`.)

We can then run the following python code to use it in Ete:

```py
from ete4 import GTDBTaxa
gtdb = GTDBTaxa()
gtdb.update_taxonomy_database("./gtdb207dump.tar.gz")
```
