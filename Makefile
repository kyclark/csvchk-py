.PHONY: test clean

PRG = "csvchk.py"

test:
	pytest -xv $(PRG) test.py 

clean:
	rm -rf .pytest_cache __pycache__
