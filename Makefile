# Regenerate words/*.json, words/index.json and the README deck list from the CSVs.
# Runs in a container, so nothing is installed on the host.
PYTHON_IMAGE := docker.io/library/python:3.13-slim

.PHONY: json
json:
	podman run --rm -v "$(CURDIR)":/work:Z -w /work $(PYTHON_IMAGE) python to_json.py
