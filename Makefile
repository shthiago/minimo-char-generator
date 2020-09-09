help:
	@echo "Functions to help managing the project"
	@echo ""
	@echo "help  :      Print this message"
	@echo "migrations:  Use alembic to run revision creation"
	@echo "migrate      Use alembic to run created migrations"
	@echo "judge:       Run pylint on src folder"
	@echo "test:        Run unit tests"
	@echo "run:         Run server with uvicorn"
	@echo "run-reload:  Run test server with uvicorn"
	@echo "coverage:         Run tests and coverage report"
	@echo

migrations:
	@alembic revision --autogenerate

migrate:
	@alembic upgrade head

judge: bandit mypy
	@pylint src/

test:
	@pytest src/

coverage:
	@coverage run  --source=src/ -m pytest src/
	@coverage report

run:
	@uvicorn --host 0.0.0.0 src.api:app

run-reload:
	@uvicorn src.api:app --reload

bandit:
	@bandit -r src/

mypy:
	@mypy src/
