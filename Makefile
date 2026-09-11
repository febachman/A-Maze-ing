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
	@echo "Development environment ready! ✅"


run:
	$(PYTHON) $(MAIN) $(CONFIG)


debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)


lint:
	$(VENV_PYTHON) -m flake8 .
	$(VENV_PYTHON) -m mypy . $(MYPY_FLAGS)
	@echo "Lint and type checks passed! ✅"


lint-strict:
	$(VENV_PYTHON) -m flake8 .
	$(VENV_PYTHON) -m mypy . --strict
	@echo "Strict type check passed! ✅"


package: install
	rm -rf build dist *.egg-info
	$(VENV_PYTHON) -m build --no-isolation
	rm -f mazegen-*.tar.gz mazegen-*.whl
	cp dist/mazegen-*.tar.gz .
	cp dist/mazegen-*.whl .
	rm -rf build dist *.egg-info
	@echo "Package built and copied to project root! ✅"


clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	@echo "Cache files cleaned! ✅"


fclean: clean
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf $(VENV)
	rm -f $(OUTPUT_TEST)
	@echo "Full clean completed! ✅"


re: fclean install all


test-package: package
	rm -rf testenv

	@echo "Testing WHL..."
	python3 -m venv testenv
	testenv/bin/pip install --index-url $(PIP_INDEX) ./mazegen-*.whl
	cd /tmp && $(CURDIR)/testenv/bin/python -c "from maze_generator import MazeGenerator; from maze_solver import MazeSolver; import maze_generator; m=MazeGenerator(20,20,seed=42,perfect=True); m.generate_maze((0,0),(19,19)); p=MazeSolver(m).path_solver((0,0),(19,19)); print('Module:', maze_generator.__file__); print('WHL OK:', p is not None)"

	rm -rf testenv

	@echo "Testing TAR.GZ..."
	python3 -m venv testenv
	testenv/bin/pip install --index-url $(PIP_INDEX) ./mazegen-*.tar.gz
	cd /tmp && $(CURDIR)/testenv/bin/python -c "from maze_generator import MazeGenerator; from maze_solver import MazeSolver; import maze_generator; m=MazeGenerator(20,20,seed=42,perfect=True); m.generate_maze((0,0),(19,19)); p=MazeSolver(m).path_solver((0,0),(19,19)); print('Module:', maze_generator.__file__); print('TAR.GZ OK:', p is not None)"


.PHONY: all install run debug lint lint-strict package \
	clean pypi fclean re test-package