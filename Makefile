PYTHON = python3
LINT = flake8
TYPECHECK = mypy --strict
MAIN = a_maze_ing.py
CONFIG = config.txt
OUTPUT_TEST = maze.txt

all: lint typecheck run

run:
	$(PYTHON) $(MAIN) $(CONFIG)

lint:
	@$(LINT) .
	@echo "Lint check passed! ✨"

typecheck:
	@$(TYPECHECK) .
	@echo "Type check passed! 🛡️"

test: lint typecheck

package:
	$(PYTHON) -m build
	@echo "Package built successfully! 📦"

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".mypy_cache" -delete
	find . -type d -name ".flake8" -delete
	find . -type d -name "dist" -delete
	find . -type d -name "build" -delete
	find . -type d -name "*.egg-info" -delete
	@echo "Object and cache files cleaned! 🧹"

fclean: clean
	rm -f $(OUTPUT_TEST)
	rm -rf *.egg-info
	@echo "Full clean completed! 🗑️"

re: fclean all

.PHONY: all run lint typecheck test package clean fclean re