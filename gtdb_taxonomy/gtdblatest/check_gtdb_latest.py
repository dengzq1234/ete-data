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


def main():
    names = ['bac120_taxonomy', 'ar53_taxonomy']

    print('Checking status of', names, '...')

    try:
        md5s_web = get_md5s()
        # The names they put in their files don't necessarily
        # corrspond to the actual files! For example, they can mention
        # ar53_taxonomy_r220.tsv.gz when the real downloadable file is
        # ar53_taxonomy.tsv.gz

        for name in names:
            md5_web = get_md5_web(md5s_web, name)
            assert md5_web, f'Cannot find mention of file for {name}'

            md5 = hashlib.md5(open(name + '.tsv.gz', 'rb').read()).hexdigest()

            print(f'  %18s is up-to-date: %s' % (name, md5 == md5_web))

    except (requests.exceptions.ConnectionError, KeyboardInterrupt,
            FileNotFoundError, ValueError, AssertionError) as e:
        sys.exit(f'Cannot check status: {e}')


def get_md5s(url='https://data.gtdb.ecogenomic.org/releases/latest/MD5SUM.txt'):
    """Return a dict like {fname: md5} from parsing the given url."""
    parts = [line.split() for line in requests.get(url).text.splitlines()]
    return {fname.lstrip('./'): md5 for md5, fname in parts}


def get_md5_web(md5s_web, name):
    pattern = name + r'.*\.tsv\.gz'
    for web_name, md5 in md5s_web.items():
        if re.match(pattern, web_name):
            return md5
    return None



if __name__ == '__main__':
    main()
