PYTHON ?= python3

.PHONY: install check fmt hooks

install:
	$(PYTHON) -m pip install -r requirements.txt

check:
	$(PYTHON) -m py_compile main.py
	$(PYTHON) -m py_compile engines/*.py requirements/*.py
	$(PYTHON) test_regressions.py

fmt:
	$(PYTHON) -m black .

hooks:
	$(PYTHON) -m pip install pre-commit
	$(PYTHON) -m pre_commit install
