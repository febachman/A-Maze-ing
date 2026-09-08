PYTHON = python3

MAIN = a_maze_ing.py
CONFIG = config.txt
OUTPUT_TEST = maze.txt

VENV = .venv
VENV_PYTHON = $(VENV)/bin/python
VENV_PIP = $(VENV_PYTHON) -m pip

MYPY_FLAGS = \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

PIP_INDEX ?= https://pypi.org/simple


all: lint run


$(VENV_PYTHON):
	$(PYTHON) -m venv $(VENV)


install: $(VENV_PYTHON)
	$(VENV_PIP) install --index-url $(PIP_INDEX) --upgrade pip
	$(VENV_PIP) install --index-url $(PIP_INDEX) \
		flake8 mypy setuptools wheel build
	@echo "Development environment ready!"


run:
	$(PYTHON) $(MAIN) $(CONFIG)


debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)


lint:
	$(VENV_PYTHON) -m flake8 .
	$(VENV_PYTHON) -m mypy . $(MYPY_FLAGS)
	@echo "Lint and type checks passed!"


lint-strict:
	$(VENV_PYTHON) -m flake8 .
	$(VENV_PYTHON) -m mypy . --strict
	@echo "Strict type check passed!"


package: install
	rm -rf build dist *.egg-info
	$(VENV_PYTHON) -m build --no-isolation
	rm -f mazegen-*.tar.gz mazegen-*.whl
	cp dist/mazegen-*.tar.gz .
	cp dist/mazegen-*.whl .
	rm -rf build dist *.egg-info
	@echo "Package built and copied to project root!"


clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	@echo "Cache files cleaned!"


pypi: $(VENV_PYTHON)
	$(VENV_PIP) install \
		--index-url https://pypi.org/simple \
		flake8 mypy setuptools wheel build
	@echo "Dependencies installed from PyPI!"


fclean: clean
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf $(VENV)
	rm -f $(OUTPUT_TEST)
	@echo "Full clean completed!"


re: fclean install all


.PHONY: all install run debug lint lint-strict package \
	clean pypi fclean re