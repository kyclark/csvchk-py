# csvchk

Check one record of a delimited text file

This program will show you the first record of a delimited text file transposed vertically.
It is meant to complement the many features of the `csvkit` tools.
For example, given a file like this:

```
$ csvlook test/test.csv
| id | val |
| -- | --- |
|  1 | foo |
|  2 | bar |
```

This program will show:

```
// ****** Record 1 ****** //
id  : 1
val : foo
```

# Usage and options

Run with `-h` or `--help` for a full usage:

	usage: csvchk [-h] [-s sep] [-f names] [-l nrecs] [-d] [-n] [-N]
	              FILE [FILE ...]

	Check a delimited text file

	positional arguments:
	  FILE                  Input file(s)

	optional arguments:
	  -h, --help            show this help message and exit
	  -s sep, --sep sep     Field separator (default: )
	  -f names, --fieldnames names
	                        Field names (no header) (default: )
	  -l nrecs, --limit nrecs
	                        How many records to show (default: 1)
	  -d, --dense           Not sparse (skip empty fields) (default: False)
	  -n, --number          Show field number (e.g., for awk) (default: False)
	  -N, --noheaders       No headers in first row (default: False)

## Separator

The default field separator is a tab character unless the input file has the extension `.csv`.
You can change this value using the `-s` or `--sep` option.

For example, given this file:

```
$ cat test/test2.txt
id:val
1:foo
2:bar
```

You could run:

```
$ csvchk -s ':' test/test2.txt
// ****** Record 1 ****** //
id  : 1
val : foo
```

## Field names

The input file is assumed to contain column headers/field names in the first row.
If a file has no such headers, you can provide a comma-separated string with `-f` or `--fieldnames` of values to use instead.

For example, given this file:

```
$ cat test/nohdr.csv
1,foo
2,bar
```

You can run:

```
$ csvchk -f 'id, value' test/nohdr.csv
// ****** Record 1 ****** //
id    : 1
value : foo
```

## Limit

By default, the program will use the `-l` or `--limit` value of `1` to show the first record.
You can increase this, for example:

```
$ csvchk -l 2 test/test.csv
// ****** Record 1 ****** //
id  : 1
val : foo
// ****** Record 2 ****** //
id  : 2
val : bar
```

To see _all_ the records, use a negative value like `-1`:

```
$ csvchk -l -1 test/test.csv
// ****** Record 1 ****** //
id  : 1
val : foo
// ****** Record 2 ****** //
id  : 2
val : bar
// ****** Record 3 ****** //
id  : 3
val : baz
```

## Dense output

By default, all fields and values will be shown for each record.
For example, given this file:

```
$ cat test/sparse.csv
id,val
1,foo
2,
,baz
```

This will be shown:

```
$ csvchk test/sparse.csv -l -1
// ****** Record 1 ****** //
id  : 1
val : foo
// ****** Record 2 ****** //
id  : 2
val :
// ****** Record 3 ****** //
id  :
val : baz
```

You can use the `-d` or `--dense` option to omit fields that have no values:

```
$ csvchk test/sparse.csv -l -1 -d
// ****** Record 1 ****** //
id  : 1
val : foo
// ****** Record 2 ****** //
id : 2
// ****** Record 3 ****** //
val : baz
```

## Numbering fields

The `-n` or `--number` option will append the field numbers before the output:

```
$ csvchk -n test/test.tab
// ****** Record 1 ****** //
  1 id  : 1
  2 val : foo
```

This can be useful if you would like to know the field number to use with `awk`, e.g., we could look for records where the `val` column (in the second position) has an "a":

```
$ awk '$2 ~ /a/' test/test.tab
id	val
2	bar
```

## No headers

If the input file does not have headers (column names) in the first row, you can use the `-N` or `--noheaders` option to have the program create names like "Field1," "Field2," etc.:

```
$ csvchk -N test/nohdr.csv
// ****** Record 1 ****** //
Field1 : 1
Field2 : foo
```

## Filter by record contents

You can use the `-g` or `--grep` option to view only records containing a string:

```
$ csvchk -g ba -l 2 tests/test.csv
// ****** Record 1 ****** //
id  : 2
val : bar
// ****** Record 2 ****** //
id  : 3
val : baz
```

## Multiple file inputs

If given multiple files as inputs, the program will insert a header noting the basename of each file:

```
$ csvchk test/test.csv test/test.tab
==> test.csv <==
// ****** Record 1 ****** //
id  : 1
val : foo

==> test.tab <==
// ****** Record 1 ****** //
id  : 1
val : foo
```

## Author

Ken Youens-Clark <kyclark@gmail.com>
