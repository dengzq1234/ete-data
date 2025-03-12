#!/usr/bin/env python3

"""
Simple script to check if the taxonomy files are up-to-date with the
latest in GTDB.

See https://github.com/etetoolkit/ete-data/blob/main/gtdb_taxonomy/README.md
for information on how to update gtdb_latest_dump.tar.gz if you need to.
"""

import sys
import re
import hashlib
import requests

URL_MD5SUM = 'https://data.gtdb.ecogenomic.org/releases/latest/MD5SUM.txt'


def main():

    names = ['bac120_taxonomy', 'ar53_taxonomy']

    print('Checking status of', names, '...')

    try:
        name_to_md5 = get_name_to_md5(URL_MD5SUM)
        # The names they put in their files don't necessarily
        # correspond to the actual files! For example, they can mention
        # ar53_taxonomy_r220.tsv.gz when the real downloadable file is
        # ar53_taxonomy.tsv.gz

        for name in names:
            md5_web = get_md5(name_to_md5, name)
            assert md5_web, f'Cannot find mention of file for {name}'

            md5 = hashlib.md5(open(name + '.tsv.gz', 'rb').read()).hexdigest()

            print(f'  %18s is up-to-date: %s' % (name, md5 == md5_web))

    except (requests.exceptions.ConnectionError, KeyboardInterrupt,
            FileNotFoundError, ValueError, AssertionError) as e:
        sys.exit(f'Cannot check status: {e}')


def get_name_to_md5(url):
    """Return a dict like {fname: md5} from parsing the given url."""
    parts = [line.split() for line in requests.get(url).text.splitlines()]
    return {fname.lstrip('./'): md5 for md5, fname in parts}


def get_md5(name_to_md5, name):
    """Return the md5 that corresponds to the given name."""
    pattern = name + r'.*\.tsv\.gz'  # name, maybe something, .tsv.gz
    for web_name, md5 in name_to_md5.items():
        if re.match(pattern, web_name):
            return md5
    return None



if __name__ == '__main__':
    main()
