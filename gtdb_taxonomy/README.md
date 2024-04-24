## How to use the GTDB database(s) in ete4

This folder contains the GTDB taxonomy data in different historical
releases, ready for use with ETE (see also [its
documentation](https://etetoolkit.github.io/ete/tutorial/tutorial_taxonomy.html#id3)
for more details).

### How to use a specific release of the GTDB database

Let's download release 207 as an example:

```
wget https://github.com/etetoolkit/ete-data/raw/main/gtdb_taxonomy/gtdb207/gtdb207dump.tar.gz
```

(Note that we download the raw dump file, `.../ete-data/raw/main/...`, and not `.../ete-data/blob/main/...`.)

We can then run the following python code to update it in ETE:

```py
from ete4 import GTDBTaxa
gtdb = GTDBTaxa()
gtdb.update_taxonomy_database("./gtdb207dump.tar.gz")
```
