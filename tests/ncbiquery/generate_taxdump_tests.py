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

    tar = tarfile.open(args.src)

    # Merged taxa ids.
    merged = read_merged(tar)
    if not args.overwrite:
        check_if_exists('merged.dmp')
    write_merged(merged, args.tids)

    # Update taxa ids, replacing the merged ones.
    tids = [merged.get(tid, tid) for tid in args.tids]

    # Nodes content, and needed taxa ids.
    nodes, children = read_nodes(tar)
    needed = find_needed(nodes, children, tids)
    if not args.overwrite:
        check_if_exists('nodes.dmp')
    write_nodes(nodes, needed)

    # Names corresponding to taxa ids.
    names = read_names(tar)
    if not args.overwrite:
        check_if_exists('names.dmp')
    write_names(names, needed)

    # Final small taxa dump.
    if not args.overwrite:
        check_if_exists(args.dest)
    create_tar(args.dest)
    print('Done. You can remove nodes.dmp names.dmp merged.dmp if you want.')

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


def read_merged(tar):
    """Read merged.dmp and return its contents as a dict."""
    print('Reading merged...')
    merged = {}
    for line in tar.extractfile('merged.dmp'):
        old, new, _ = [x.strip() for x in line.decode().split('|')]
        merged[old] = new

    return merged


def write_merged(merged, tids):
    """Write merged.dmp with only the relevant taxa ids."""
    print('Writing merged.dmp ...')
    with open('merged.dmp', 'wt') as fmerged:
        for tid in tids:
            if tid in merged:
                fmerged.write(f'{tid}\t|\t{merged[tid]}\t|\n')


def read_nodes(tar):
    """Read nodes.dmp, return it as a dict, and a dict from id to children."""
    print('Reading nodes...')
    nodes = {}
    children = {}
    for line in tar.extractfile('nodes.dmp'):
        tid, ptid, *rest = [x.strip() for x in line.decode().split('|')]
        nodes[tid] = [ptid] + rest
        if ptid:  # parent taxa id
            children.setdefault(ptid, set()).add(tid)

    return nodes, children


def find_needed(nodes, children, tids):
    """Return the taxa ids of all nodes to fully cover tids."""
    # Add tids and all their ancestors.
    needed = {'1'}  # all the taxa ids that we need to get to our tids
    for tid in tids:
        while True:
            needed.add(tid)
            tid = nodes[tid][0]
            if tid in needed:
                break

    # Add all descendants.
    extending = set(tids)
    while extending:
        ch = children.get(extending.pop())
        if ch:
            extending |= ch
            needed |= ch

    return sorted(needed)  # so they appear in order


def write_nodes(nodes, needed):
    """Write nodes.dmp with only the needed taxa ids."""
    print('Writing nodes.dmp ...')
    with open('nodes.dmp', 'wt') as fnodes:
        for tid in needed:
            fnodes.write('\t|\t'.join([tid] + nodes[tid]) + '\n')


def read_names(tar):
    """Read names.dmp and return its contents as a dict."""
    print('Reading names...')
    names = {}
    for line in tar.extractfile('names.dmp'):
        tid, *rest = [x.strip() for x in line.decode().split('|')]
        names.setdefault(tid, []).append(rest)

    return names


def write_names(names, needed):
    """Write names.dmp with only the needed taxa ids."""
    print('Writing names.dmp ...')
    with open('names.dmp', 'wt') as fnames:
        for tid in needed:
            for results in names[tid]:
                fnames.write('\t|\t'.join([tid] + results) + '\n')


def create_tar(fname):
    """Put it all in the given filename."""
    print(f'Creating {fname} ...')
    os.system(f'tar -vczf {fname} merged.dmp nodes.dmp names.dmp')


def check_if_exists(fname):
    if os.path.exists(fname):
        try:
            answer = input('File %s already exists. Overwrite? [y/n] ' % fname)
            assert answer.lower().startswith('y')
        except (KeyboardInterrupt, AssertionError):
            sys.exit('\nCancelling.')



if __name__ == '__main__':
    main()
