#!/usr/bin/env python3
"""
Purpose: Check the first/few records of a delimited text file
Author : Ken Youens-Clark <kyclark@gmail.com>
"""

import argparse
import csv
import os
import re
import sys


# --------------------------------------------------
def get_args():
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

    args = parser.parse_args()

    for filename in args.file:
        if not os.path.isfile(filename):
            parser.error(f"No such file or directory: '{filename}'")

    args.file = list(map(lambda f: open(f, encoding=args.encoding), args.file))

    if len(args.sep) > 1:
        parser.error(f'--sep "{args.sep}" must be a 1-character string')

    return args


# --------------------------------------------------
def main():
    """ Make a jazz noise here """

    args = get_args()

    for i, fh in enumerate(args.file):
        if len(args.file) > 1:
            print('{}==> {} <=='.format('\n' if i > 0 else '',
                                        os.path.basename(fh.name)))

        sep = guess_sep(args.sep, fh.name)
        csv_args = {'delimiter': sep}

        if args.fieldnames:
            names = re.split(r'\s*,\s*', args.fieldnames)
            if names:
                csv_args['fieldnames'] = names

        if args.noheaders:
            num_flds = len(fh.readline().split(sep))
            csv_args['fieldnames'] = list(
                map(lambda i: f'Field{i}', range(1, num_flds + 1)))
            fh.seek(0)

        reader = csv.DictReader(fh, **csv_args)

        for rec_num, row in enumerate(reader, start=1):
            vals = dict([x for x in row.items()
                         if x[1] != '']) if args.dense else row
            flds = vals.keys()
            longest = max(map(len, flds))
            fmt = '{:' + str(longest + 1) + '}: {}'
            print(f'// ****** Record {rec_num} ****** //')
            for n, (key, val) in enumerate(vals.items(), start=1):
                show = fmt.format(key, val)
                if args.number:
                    print('{:3} {}'.format(n, show))
                else:
                    print(show)

            if rec_num == args.limit:
                break


# --------------------------------------------------
def guess_sep(sep, filename):
    """ If no separator, guess from file extension """

    if not sep:
        _, ext = os.path.splitext(filename)
        if ext == '.csv':
            sep = ','
        else:
            sep = '\t'

    return sep


# --------------------------------------------------
def test_guess_sep():
    """ Test guess_sep() """

    assert guess_sep(',', 'foo.csv') == ','
    assert guess_sep('', 'foo.csv') == ','
    assert guess_sep('\t', 'foo.csv') == '\t'
    assert guess_sep('', 'foo.tab') == '\t'
    assert guess_sep('', 'foo.txt') == '\t'


# --------------------------------------------------
if __name__ == '__main__':
    main()
