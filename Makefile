update-deps:
	pip install pip-tools
	pip-compile --build-isolation requirements/dev.in --output-file requirements/dev.txt
	pip-compile --build-isolation requirements/requirements.in --output-file requirements/requirements.txt

build:
	@docker-compose -f docker-compose.yml up --force-recreate --build

up:
	@docker-compose -f docker-compose.yml up

test:
	@docker-compose -f docker-compose.yml exec backend pytest -s -vv
