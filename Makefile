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
	@clear
	@echo "$(YELLOW) → Installing dependencies...$(RESET)"
	@$(UV) sync
	@echo "$(GREEN) ✓ Done $(RESET)"

run: $(PACMAN) $(CONFIG)
	@echo "$(YELLOW) → Loading PAC•MAN...$(RESET)"
	@$(UV) run $(PYTHON) $^

debug: $(PACMAN) $(CONFIG)
	@echo "$(YELLOW) → Entering debugger...$(RESET)"
	@$(UV) run $(PYTHON) -m pdb $^

lint:
	@echo "$(YELLOW) → Running flake8...$(RESET)"
	@$(UV) run flake8 $(PACMAN) src/
	@echo "$(YELLOW)→ Running mypy...$(RESET)"
	@$(UV) run mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs $(PACMAN) src/ \
	&& echo "$(GREEN) ✓ Lint passed.$(RESET)" || echo "$(RED) ✗ Merda.$(RESET)"


lint-strict:
	@echo "$(YELLOW) → Running flake8...$(RESET)"
	@$(UV) run flake8 $(PACMAN) src/
	@echo "$(YELLOW) → Running mypy --strict...$(RESET)"
	@$(UV) run mypy --strict $(PACMAN) src/ \
	&& echo "$(GREEN) ✓ Lint passed.$(RESET)" || echo "$(RED) ✗ Merda.$(RESET)"

check-docstrings:
	clear
	@echo "$(YELLOW) → Checking docstrings...$(RESET)"
	@$(UV) run pydocstyle $(PACMAN) src/ \
	&& echo "$(GREEN) ✓ Docstrings are valid.$(RESET)" || echo "$(RED) ✗ Merda.$(RESET)"

clean:
	@echo "$(YELLOW) → Cleaning caches...$(RESET)"
	@find . -type d -name "__pycache__" -not -path "./.venv/*" | xargs rm -rf
	@find . -type d -name ".mypy_cache" -not -path "./.venv/*" | xargs rm -rf
	@find . -type d -name "*.egg-info"  -not -path "./.venv/*" | xargs rm -rf
	@find . -type d -name ".ruff_cache" -not -path "./.venv/*" | xargs rm -rf
	@echo "$(GREEN) ✓ Sto gran cazzo$(RESET)"

fclean: clean
	@clear
	@echo "$(YELLOW) → Cleaning also build and dist...$(RESET)"
	@rm -rf dist/ build/
	@echo "$(GREEN) ✓ Sto gran cazzo$(RESET)"

build:
	@$(UV) run pyinstaller --onefile --name pac-man pac-man.py
	@cp -r assets dist/assets
	@cp config.json dist/config.json
	@cp -r game_data dist/game_data
	@echo "$(GREEN) ✓ sto gran cazzo $(RESET)"
