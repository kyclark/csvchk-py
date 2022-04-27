""" Tests for csvchk.py """

import os
import random
import re
import string
from subprocess import getstatusoutput

prg = './csvchk.py'
csv1 = './tests/test.csv'
tab1 = './tests/test.tab'
txt1 = './tests/test.txt'
txt2 = './tests/test2.txt'
nohdr_csv = './tests/nohdr.csv'
nohdr_tab = './tests/nohdr.txt'
sparse = './tests/sparse.csv'
iso = './tests/test-iso-8859-1.csv'
duplicate_cols = './tests/duplicate_cols.csv'


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{prg} {flag}')
        assert rv == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_bad_file():
    """test bad file"""

    bad = random_string()
    rv, out = getstatusoutput(f'{prg} {bad}')
    assert rv != 0
    assert out.lower().startswith('usage')
    assert re.search(f"No such file or directory: '{bad}'", out)


# --------------------------------------------------
def test_bad_sep():
    """test bad sep"""

    sep = random.choice(',!:@') * random.choice(range(2, 5))
    print(f">>>> {sep}")
    rv, out = getstatusoutput(f'{prg} -s "{sep}" {txt1}')
    assert rv != 0
    assert out.lower().startswith('usage')
    assert re.search(f'--sep "{sep}" must be a 1-character string', out)


# --------------------------------------------------
def test_csv():
    """test"""

    rv, out = getstatusoutput(f'{prg} {csv1}')
    assert rv == 0
    assert out.strip() == '\n'.join(
        ['// ****** Record 1 ****** //', 'id  : 1', 'val : foo'])


# --------------------------------------------------
def test_tab():
    """test"""

    rv, out = getstatusoutput(f'{prg} {tab1}')
    assert rv == 0
    assert out.strip() == '\n'.join(
        ['// ****** Record 1 ****** //', 'id  : 1', 'val : foo'])


# --------------------------------------------------
def test_sep():
    """test"""

    for file, sep in [(txt1, ','), (txt2, ':')]:
        rv, out = getstatusoutput(f'{prg} -s "{sep}" {file}')
        assert rv == 0
        assert out.strip() == '\n'.join(
            ['// ****** Record 1 ****** //', 'id  : 1', 'val : foo'])


# --------------------------------------------------
def test_iso():
    """test iso"""

    rv, out = getstatusoutput(f'{prg} {iso} -e ISO-8859-1')
    assert rv == 0
    assert out.strip() == '\n'.join([
        '// ****** Record 1 ****** //', 'Sample ID : TC10-2L',
        'Treatment : Tailings + 10 % Compost', 'Be (µg/g) : 0.009078679'
    ])


# --------------------------------------------------
def test_number():
    """test"""

    rv, out = getstatusoutput(f'{prg} -n {csv1}')
    assert rv == 0
    assert out.strip() == '\n'.join(
        ['// ****** Record 1 ****** //', '  1 id  : 1', '  2 val : foo'])


# --------------------------------------------------
def test_no_headers_csv():
    """test"""

    rv, out = getstatusoutput(f'{prg} -N {nohdr_csv}')
    assert rv == 0
    assert out.strip() == '\n'.join(
        ['// ****** Record 1 ****** //', 'Field1 : 1', 'Field2 : foo'])


# --------------------------------------------------
def test_no_headers_tab():
    """test"""

    rv, out = getstatusoutput(f'{prg} -N {nohdr_tab}')
    assert rv == 0
    assert out.strip() == '\n'.join(
        ['// ****** Record 1 ****** //', 'Field1 : 1', 'Field2 : foo'])


# --------------------------------------------------
def test_fieldnames():
    """test"""

    rv, out = getstatusoutput(f'{prg} -f "f1, f2" {nohdr_csv}')
    assert rv == 0
    assert out.strip() == '\n'.join(
        ['// ****** Record 1 ****** //', 'f1 : 1', 'f2 : foo'])


# --------------------------------------------------
def test_limit():
    """test"""

    rv, out = getstatusoutput(f'{prg} -l 2 {csv1}')
    assert rv == 0
    assert out.strip() == '\n'.join([
        '// ****** Record 1 ****** //', 'id  : 1', 'val : foo',
        '// ****** Record 2 ****** //', 'id  : 2', 'val : bar'
    ])


# --------------------------------------------------
def test_negative_limit():
    """test"""

    rv, out = getstatusoutput(f'{prg} -l -1 {csv1}')
    assert rv == 0
    assert out.strip() == '\n'.join([
        '// ****** Record 1 ****** //', 'id  : 1', 'val : foo',
        '// ****** Record 2 ****** //', 'id  : 2', 'val : bar',
        '// ****** Record 3 ****** //', 'id  : 3', 'val : baz'
    ])


# --------------------------------------------------
def test_grep():
    """test grep"""

    rv1, out1 = getstatusoutput(f'{prg} -g ba {csv1}')
    assert rv1 == 0
    assert out1.strip() == '\n'.join([
        '// ****** Record 1 ****** //',
        'id  : 2',
        'val : bar',
    ])

    rv2, out2 = getstatusoutput(f'{prg} --grep ba --limit 10 {csv1}')
    assert rv2 == 0
    assert out2.strip() == '\n'.join([
        '// ****** Record 1 ****** //',
        'id  : 2',
        'val : bar',
        '// ****** Record 2 ****** //',
        'id  : 3',
        'val : baz',
    ])


# --------------------------------------------------
def test_dense():
    """test"""

    rv, out = getstatusoutput(f'{prg} -l 3 -d {sparse}')
    assert rv == 0
    assert out.strip() == '\n'.join([
        '// ****** Record 1 ****** //', 'id  : 1', 'val : foo',
        '// ****** Record 2 ****** //', 'id : 2',
        '// ****** Record 3 ****** //', 'val : baz'
    ])


# --------------------------------------------------
def test_multiple_files():
    """test"""

    rv, out = getstatusoutput(f'{prg} {csv1} {tab1}')
    assert rv == 0
    expected = '\n'.join([
        '==> test.csv <==',
        '// ****** Record 1 ****** //',
        'id  : 1',
        'val : foo',
        '',
        '==> test.tab <==',
        '// ****** Record 1 ****** //',
        'id  : 1',
        'val : foo',
    ])
    assert out.strip() == expected


# --------------------------------------------------
def test_duplicate_cols():
    """test"""

    rv, out = getstatusoutput(f'{prg} {duplicate_cols}')
    assert rv == 0
    expected = '\n'.join([
        '// ****** Record 1 ****** //',
        'name  : Keith',
        'age   : 42',
        'age_2 : 42',
    ])
    assert out.strip() == expected


# --------------------------------------------------
def random_string():
    """generate a random string"""

    k = random.randint(5, 10)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))
