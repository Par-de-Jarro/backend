install: install_python install_project install_precommit

install_python:
	pyenv install 3.10.3 --skip-existing
	pyenv local 3.10.3

install_project:
	poetry env use 3.10.3
	poetry install

install_precommit:
	poetry run pre-commit install --install-hooks

update:
	poetry update

test:
	poetry run pytest $(file)

test-docker:
	docker compose run --rm server pytest $(file)

test-cov:
	poetry run pytest \
		--cov-report html \
		--cov-report xml:cov.xml \
		--cov-report term-missing \
		--cov=app


docker-alembic-revision:
	docker compose run server alembic revision --autogenerate -m $(m)

lint:
	poetry run pre-commit run --all-files

start:
	poetry run uvicorn app.main:app --reload