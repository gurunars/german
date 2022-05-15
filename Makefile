process: venv
	venv/bin/python process.py

venv:
	virtualenv venv
	./venv/bin/pip install -r requirements.txt

test: venv
	./venv/bin/pytest -svv --doctest-modules process.py

.PHONY: test
