#!/usr/bin/env python3

"""
Simple script to check if the taxonomy files are up-to-date with the
latest in GTDB.

See https://github.com/etetoolkit/ete-data/blob/main/README.md for
information on how to update gtdb_latest_dump.tar.gz if you need to.
"""

import sys
import hashlib
import requests


def main():
    fnames = ['bac120_taxonomy.tsv.gz', 'ar53_taxonomy.tsv.gz']

    print('Checking status of files', fnames, '...')

    try:
        md5s_web = get_md5s()
        for fname in fnames:
            md5 = hashlib.md5(open(fname, 'rb').read()).hexdigest()
            print(f'  %22s is up-to-date: %s' % (fname, md5 == md5s_web[fname]))
    except KeyError as e:
        sys.exit(f'Cannot find mention of file: {e}')
    except (requests.exceptions.ConnectionError, KeyboardInterrupt,
            FileNotFoundError, ValueError) as e:
        sys.exit(f'Cannot check status: {e}')


def get_md5s(url='https://data.gtdb.ecogenomic.org/releases/latest/MD5SUM.txt'):
    """Return a dict like {fname: md5} from parsing the given url."""
    parts = [line.split() for line in requests.get(url).text.splitlines()]
    return {fname.lstrip('./'): md5 for md5, fname in parts}



if __name__ == '__main__':
    main()
