.PHONY: test clean dist test_upload test_install upload

PRG = "csvchk.py"

test:
	python3 -m pytest --pylint -xv $(PRG) tests

dist: clean
	python3 -m build

clean:
	rm -rf dist *.egg-info build .pytest_cache __pycache__

up:
	python3 -m twine upload --repository pypi dist/*

prereq:
	python3 -m pip install -r requirements.txt
