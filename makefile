PY=python3
PIP=$(PY) -m pip
VENV=.venv
ACTIVATE=$(VENV)/bin/activate
REQ=requirements.txt

.PHONY: help venv install run clean

help:
	@echo "Targets: venv install run clean"

venv:
	$(PY) -m venv $(VENV)
	@echo "venv created at $(VENV). You can activate with 'source $(ACTIVATE)'"

install: venv
	. $(ACTIVATE) && $(PIP) install --upgrade pip
	@if [ -f $(REQ) ]; then . $(ACTIVATE) && $(PIP) install -r $(REQ); fi

run: 
	$(VENV)/bin/$(PY) -m src.check_jobs

clean:
	rm -rf $(VENV)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +