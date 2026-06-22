PYTHON = python3
UV = uv
CONFIG = config.json
PACMAN = pac-man.py

RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RESET := \033[0m



all: install run clean

install:
	$(UV) sync

run: $(PACMAN) $(CONFIG)
	$(UV) run $(PYTHON) $^

debug: $(PACMAN) $(CONFIG)
	$(UV) run $(PYTHON) -m pdb $^

lint:
	$(UV) run flake8 $(PACMAN) src/
	$(UV) run mypy $(PACMAN) src/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@$(UV) run flake8 $(PACMAN) src/
	@$(UV) run mypy $(PACMAN) src/

clean:
	@echo "$(YELLOW) → Cleaning caches...$(RESET)"
	@find . -type d -name "__pycache__" -not -path "./.venv/*" | xargs rm -rf
	@find . -type d -name ".mypy_cache" -not -path "./.venv/*" | xargs rm -rf
	@find . -type d -name "*.egg-info"  -not -path "./.venv/*" | xargs rm -rf
	@find . -type d -name ".ruff_cache" -not -path "./.venv/*" | xargs rm -rf
	@echo "$(GREEN) ✓ Sto gran cazzo$(RESET)"
