PYTHON = python3
PIP = $(PYTHON) -m pip

MAIN = a_maze_ing.py
CONFIG = config.txt
OUTPUT_TEST = maze.txt

BUILDENV = buildenv
TESTENV = testenv

BUILD_PYTHON = $(BUILDENV)/bin/python
TEST_PYTHON = $(TESTENV)/bin/python

MYPY_FLAGS = \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs


all: lint


install:
	$(PIP) install flake8 mypy build


run:
	$(PYTHON) $(MAIN) $(CONFIG)


debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)


lint:
	flake8 .
	mypy . $(MYPY_FLAGS)
	@echo "Lint and type checks passed! ✨"


lint-strict:
	flake8 .
	mypy . --strict
	@echo "Strict type check passed! 🛡️"


typecheck:
	mypy . --strict
	@echo "Type check passed! 🛡️"


test: lint
	@echo "All checks passed! ✅"


package:
	rm -rf build dist *.egg-info
	rm -f mazegen-*.tar.gz mazegen-*.whl
	$(PYTHON) -m build
	cp dist/mazegen-*.tar.gz .
	cp dist/mazegen-*.whl .
	rm -rf build dist *.egg-info
	@echo "Package built and copied to project root! 📦"


build-package:
	rm -rf $(BUILDENV)
	rm -rf build dist *.egg-info
	rm -f mazegen-*.tar.gz mazegen-*.whl
	$(PYTHON) -m venv $(BUILDENV)
	$(BUILD_PYTHON) -m pip install --upgrade pip
	$(BUILD_PYTHON) -m pip install build
	$(BUILD_PYTHON) -m build
	cp dist/mazegen-*.tar.gz .
	cp dist/mazegen-*.whl .
	rm -rf $(BUILDENV)
	rm -rf build dist *.egg-info
	@echo "Package built in isolated environment! 📦"


test-package:
	rm -rf $(TESTENV)
	$(PYTHON) -m venv $(TESTENV)
	$(TEST_PYTHON) -m pip install ./mazegen-*.whl
	$(TEST_PYTHON) -c "from maze_generator import MazeGenerator; print('MazeGenerator import OK ✅')"
	$(TEST_PYTHON) -c "from maze_solver import MazeSolver; print('MazeSolver import OK ✅')"
	rm -rf $(TESTENV)
	@echo "Package tested successfully! ✅"


package-check: build-package test-package
	@echo "Build and installation test completed! 🎉"


clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	@echo "Cache files cleaned! 🧹"


fclean: clean
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf $(BUILDENV)
	rm -rf $(TESTENV)
	rm -f $(OUTPUT_TEST)
	@echo "Full clean completed! 🗑️"


re: fclean all


.PHONY: all install run debug lint lint-strict typecheck test \
	package build-package test-package package-check \
	clean fclean re