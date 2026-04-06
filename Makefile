PYTHON ?= python3

.PHONY: test audit

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

audit:
	PYTHONPATH=src $(PYTHON) -m se_traceability_lab.cli audit --data-dir data --export-dir reports

