PYTHON ?= python3

.PHONY: test audit roadmap

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

audit:
	PYTHONPATH=src $(PYTHON) -m se_traceability_lab.cli audit --data-dir data --export-dir reports

roadmap:
	PYTHONPATH=src $(PYTHON) -m se_traceability_lab.cli roadmap --projects-file data/portfolio_projects.json --export-path reports/portfolio-roadmap.md
