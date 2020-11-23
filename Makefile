process: venv
	venv/bin/python process.py

venv:
	python -m venv venv
	./venv/bin/pip install -r requirements.txt

test:
	./venv/bin/pytest -svv --doctest-modules process.py

.PHONY: test
