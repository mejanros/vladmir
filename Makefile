PYTHON=python3

setup:
	@echo "Environment creation and intalling main dependecies"
	@$(PYTHON) -m venv vlad_env

install:
	pip install -r requirements.txt

system-deps:
	@sudo apt-get update
	@sudo apt install sra-toolkit