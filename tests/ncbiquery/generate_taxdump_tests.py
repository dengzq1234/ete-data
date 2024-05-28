#!/usr/bin/env python3

"""
Generate a small taxdump_tests.tar.gz to use with ete's tests, starting from
a taxdump.tar.gz downloaded from the NCBI.

This allows the related ete tests (like tests/test_ncbiquery.py) to go fast,
and the user does not have to download big files just to run them.
"""

import sys
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter as fmt
import tarfile


def main():
    args = get_args()

    if not os.path.exists(args.src):
        url = 'https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz'
        sys.exit(f'Missing {args.src} -- you can download it from {url}')

    print('Using full taxdump file:', args.src)
    tar = tarfile.open(args.src)

    print('Taxa ids to include:', ' '.join(args.tids))

    # Merged taxa ids.
    print('Reading all merged ids...')
    merged = read_merged(tar)

    if not args.overwrite:
        check_if_exists('merged.dmp')
    print('Writing relevant ids to merged.dmp ...')
    write_merged(merged, args.tids)

    # Update taxa ids, replacing the merged ones.
    tids = [merged.get(tid, tid) for tid in args.tids]

    # Nodes and needed taxa ids.
    print('Reading all nodes...')
    nodes, children = read_nodes(tar)

    needed = find_needed(nodes, children, tids)

    print('Writing nodes with needed ids to nodes.dmp ...')
    if not args.overwrite:
        check_if_exists('nodes.dmp')
    write_nodes(nodes, needed)

    # Names.
    print('Reading all names...')
    names = read_names(tar)

    if not args.overwrite:
        check_if_exists('names.dmp')
    print('Writing names with needed ids to names.dmp ...')
    write_names(names, needed)

    # Final taxa dump (a smaller file than the original full taxa dump).
    if not args.overwrite:
        check_if_exists(args.dest)
    print(f'Creating {args.dest} ...')
    os.system(f'tar -vczf "{args.dest}" merged.dmp nodes.dmp names.dmp')

    print('Done. You can safely remove: merged.dmp nodes.dmp names.dmp')

    # If we want to create the sqlite file from it, we would do:
    #   from ete4.ncbi_taxonomy import ncbiquery
    #   ncbiquery.update_db('test_ncbiquery.taxa.sqlite',
    #                       'taxdump_tests.tar.gz')


def get_args():
    """Return the parsed command-line arguments."""
    parser = ArgumentParser(description=__doc__, formatter_class=fmt)
    add = parser.add_argument  # shortcut

    add('--src', default='taxdump.tar.gz', help='source file (full NCBI dump)')
    add('--dest', default='taxdump_tests.tar.gz', help='destination file')
    add('--tids', metavar='ID', nargs='+', help='taxa ids to include',
        default=['9604', '9605', '9606', '649756', '7507', '678',
                 '42099', '9443', '9598', '10090'])
    add('--overwrite', action='store_true', help='overwrite files (skip checks)')

    return parser.parse_args()


def extract(tar, fname):
    """Yield fields extracted from file fname in the tar file."""
    # The lines look like:
    # x0	|	x1	|	...	|	xn	|
    for line in tar.extractfile(fname):
        yield [x.strip() for x in line.decode().split('|')[:-1]]
        # The  [:-1]  is because there is nothing after the last "|"


def read_merged(tar):
    """Read merged.dmp and return its contents as a dict."""
    # The lines look like:
    # 42099	|	907947	|
    return dict(extract(tar, 'merged.dmp'))  # like  {'42099': '907947', ...}


def write_merged(merged, tids):
    """Write merged.dmp with only the relevant taxa ids."""
    with open('merged.dmp', 'wt') as fmerged:
        for tid in tids:
            if tid in merged:
                fmerged.write(f'{tid}\t|\t{merged[tid]}\t|\n')


def read_nodes(tar):
    """Read nodes.dmp, return it as a dict, and a dict from id to children."""
    # The lines look like:
    # 678	|	2614977	|	species	|	...	|

    nodes = {}  # will look like  nodes['678'] = ['2614977', 'species', ...]
    children = {}  # will look like  children['2614977'] = {'678', ...}
    for tid, ptid, *rest in extract(tar, 'nodes.dmp'):
        nodes[tid] = [ptid] + rest
        if ptid:  # parent taxa id
            children.setdefault(ptid, set()).add(tid)

    return nodes, children


def find_needed(nodes, children, tids):
    """Return the taxa ids of all nodes to fully cover tids."""
    # Add tids and all their ancestors.
    needed = {'1'}  # all the taxa ids that we need to get to our tids
    for tid in tids:
        while tid not in needed:  # keep adding ids until we find a saved one
            needed.add(tid)
            tid = nodes[tid][0]  # go to its parent taxa id

    # Add all descendants.
    extending = set(tids)
    while extending:
        ch = children.get(extending.pop())
        if ch:
            extending |= ch
            needed |= ch

    return sorted(needed, key=int)  # so they appear in order


def write_nodes(nodes, needed):
    """Write nodes.dmp with only the needed taxa ids."""
    with open('nodes.dmp', 'wt') as fnodes:
        for tid in needed:
            fnodes.write('\t|\t'.join([tid] + nodes[tid]) + '\t|\n')


def read_names(tar):
    """Read names.dmp and return its contents as a dict."""
    # Each taxa id can have several entries. The lines look like:
    # 9606	|	human	|		|	genbank common name	|
    # 9606	|	Homo sapiens	|		|	scientific name	|

    names = {}  # will look like  names['9606'] = [['human', ...], ['Homo sapiens', ...], ...]
    for tid, *rest in extract(tar, 'names.dmp'):
        names.setdefault(tid, []).append(rest)

    return names


def write_names(names, needed):
    """Write names.dmp with only the needed taxa ids."""
    with open('names.dmp', 'wt') as fnames:
        for tid in needed:
            for results in names[tid]:
                fnames.write('\t|\t'.join([tid] + results) + '\t|\n')


def check_if_exists(fname):
    if os.path.exists(fname):
        try:
            answer = input(f'File {fname} already exists. Overwrite? [y/n] ')
            assert answer.lower().startswith('y')
        except (KeyboardInterrupt, EOFError, AssertionError):
            sys.exit('\nCancelling.')



if __name__ == '__main__':
    main()
