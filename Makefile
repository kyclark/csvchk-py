.PHONY: test clean dist test_upload test_install upload

PRG = "csvchk.py"

test:
	python3 -m pytest --pylint -xv $(PRG) tests

dist: clean
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf dist *.egg-info build .pytest_cache __pycache__

test_upload: dist
    python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

test_install:
	(cd ~ && python3 -m pip install --index-url https://test.pypi.org/csvchk/ --no-deps csvchk)

up:
	twine upload dist/*

prereq:
	python3 -m pip install -r requirements.txt
