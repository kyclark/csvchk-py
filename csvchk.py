#!/usr/bin/env python3
"""
Purpose: Check the first/few records of a delimited text file
Author : Ken Youens-Clark <kyclark@gmail.com>
"""

import argparse
import csv
import os
import pyparsing as pp
import re
import sys
from typing import List, TextIO, NamedTuple, Any, Dict

VERSION = '0.1.8'


class Args(NamedTuple):
    file: List[TextIO]
    sep: str
    fieldnames: str
    limit: int
    grep: str
    dense_view: bool
    show_field_number: bool
    no_headers: bool


# --------------------------------------------------
def get_args() -> Args:
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Check a delimited text file',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        type=str,
                        nargs='+',
                        help='Input file(s)')

    parser.add_argument('-s',
                        '--sep',
                        help='Field separator',
                        metavar='sep',
                        type=str,
                        default='')

    parser.add_argument('-f',
                        '--fieldnames',
                        help='Field names (no header)',
                        metavar='names',
                        type=str,
                        default='')

    parser.add_argument('-l',
                        '--limit',
                        help='How many records to show',
                        metavar='nrecs',
                        type=int,
                        default=1)

    parser.add_argument('-g',
                        '--grep',
                        help='Only show records with a given value',
                        metavar='grep',
                        type=str,
                        default='')

    parser.add_argument('-d',
                        '--dense',
                        help='Not sparse (skip empty fields)',
                        action='store_true')

    parser.add_argument('-n',
                        '--number',
                        help='Show field number (e.g., for awk)',
                        action='store_true')

    parser.add_argument('-N',
                        '--noheaders',
                        help='No headers in first row',
                        action='store_true')

    parser.add_argument('-e',
                        '--encoding',
                        help='File encoding',
                        metavar='encode',
                        type=str,
                        choices=['utf-8', 'utf-8-sig', 'ISO-8859-1'],
                        default='utf-8')

    parser.add_argument('--version',
                        action='version',
                        version=f'%(prog)s {VERSION}')

    args = parser.parse_args()

    for filename in args.file:
        if filename != '-' and not os.path.isfile(filename):
            parser.error(f"No such file or directory: '{filename}'")

    open_args = {'encoding': args.encoding, 'errors': 'ignore'}
    args.file = list(
        map(lambda f: sys.stdin
            if f == '-' else open(f, **open_args), args.file))

    if len(args.sep) > 1:
        parser.error(f'--sep "{args.sep}" must be a 1-character string')

    return Args(file=args.file,
                sep=args.sep,
                fieldnames=args.fieldnames,
                limit=args.limit,
                grep=args.grep,
                dense_view=args.dense,
                show_field_number=args.number,
                no_headers=args.noheaders)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    grep = args.grep

    for i, fh in enumerate(args.file):
        if len(args.file) > 1:
            print('{}==> {} <=='.format('\n' if i > 0 else '',
                                        os.path.basename(fh.name)))

        sep = guess_sep(args.sep, fh.name)
        csv_args: Dict[str, Any] = {'delimiter': sep}

        if args.fieldnames:
            names = re.split(r'\s*,\s*', args.fieldnames)
            if names:
                csv_args['fieldnames'] = names

        if args.no_headers:
            line = fh.readline()
            num_flds = len(pp.commaSeparatedList.parseString(line).asList())
            csv_args['fieldnames'] = list(
                map(lambda i: f'Field{i}', range(1, num_flds + 1)))
            if fh.name != '<stdin>':
                fh.seek(0)

        reader = csv.DictReader(fh, **csv_args)

        num_shown = 0
        for row in reader:
            vals = dict([x for x in row.items()
                         if x[1] != '']) if args.dense_view else row

            if grep and not any([grep in x for x in vals.values()]):
                continue

            flds = vals.keys()
            longest = max(map(len, flds))
            fmt = '{:' + str(longest + 1) + '}: {}'
            num_shown += 1
            print(f'// ****** Record {num_shown} ****** //')
            for n, (key, val) in enumerate(vals.items(), start=1):
                show = fmt.format(key, val)
                if args.show_field_number:
                    print('{:3} {}'.format(n, show))
                else:
                    print(show)

            if num_shown == args.limit:
                break


# --------------------------------------------------
def guess_sep(sep: str, filename: str) -> str:
    """ If no separator, guess from file extension """

    if not sep:
        _, ext = os.path.splitext(filename)
        if ext == '.csv':
            sep = ','
        else:
            sep = '\t'

    return sep


# --------------------------------------------------
def test_guess_sep() -> None:
    """ Test guess_sep() """

    assert guess_sep(',', 'foo.csv') == ','
    assert guess_sep('', 'foo.csv') == ','
    assert guess_sep('\t', 'foo.csv') == '\t'
    assert guess_sep('', 'foo.tab') == '\t'
    assert guess_sep('', 'foo.txt') == '\t'


# --------------------------------------------------
if __name__ == '__main__':
    main()
