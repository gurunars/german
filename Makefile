# Regenerate words/*.json, words/index.json and the README deck list from the CSVs.
# Runs in a container, so nothing is installed on the host.
PYTHON_IMAGE := docker.io/library/python:3.13-slim

# `make forms` fetches the inflection tables of sentences/lemmas.tsv (needs the network).
.PHONY: json forms
json:
	podman run --rm -v "$(CURDIR)":/work:Z -w /work $(PYTHON_IMAGE) sh -c "python to_json.py && python lessons.py"

forms:
	podman run --rm -v "$(CURDIR)":/work:Z -w /work $(PYTHON_IMAGE) python forms.py
