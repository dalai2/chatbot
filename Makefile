.PHONY: help install test run down clean

# Detect Windows (Git Bash will still return "MINGW64_NT" but we check for it)
ifeq ($(OS),Windows_NT)
    PYTHON = python
    VENV_PYTHON = venv/Scripts/python.exe
else
    PYTHON = python3
    VENV_PYTHON = venv/bin/python
endif

help:
	@echo "Available commands:"
	@echo "  make install: Install requirements."
	@echo "  make test: Run tests."
	@echo "  make run: Run the service in Docker."
	@echo "  make down: Teardown running services."
	@echo "  make clean: Teardown and remove containers."

install:
	@echo "Installing requirements..."
	@if [ ! -d "venv" ]; then $(PYTHON) -m venv venv; fi
	@$(VENV_PYTHON) -m pip install --upgrade pip
	@$(VENV_PYTHON) -m pip install -r requirements.txt

test:
	@echo "Running tests..."
	@$(VENV_PYTHON) -m pytest app/tests.py

run:
	@echo "Running Docker containers..."
	docker compose up --build

down:
	@echo "Stopping Docker containers..."
	docker compose down

clean:
	@echo "Stopping and removing Docker containers..."
	docker compose down --rmi local
