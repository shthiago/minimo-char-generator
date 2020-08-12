help:
	@echo "Functions to help managing the project"
	@echo ""
	@echo "help: Print this message"
	@echo "migrations: use alembic to run revision creation"
	@echo "migrate: use alembic to run created migrations"
	@echo "judge: run pylint on src folder"
	@echo "test: run unit tests"

migrations:
	@alembic revision --autogenerate

migrate:
	@alembic upgrade head

judge:
	@pylint src/

test:
	@pytest src/