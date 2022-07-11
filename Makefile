#########################
# DEFAULTS
#########################
GUINICORN_PORT = 8000
GUINICORN_WORKERS = 1
GUINICORN_TIME_OUT = 123

#################################################################################
# COMMANDS                                                                      #
#################################################################################
format:
	set -e
	isort --recursive  --force-single-line-imports app tests
	autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place app tests
	black app tests
	isort --recursive app tests

lint:
	set -e
	set -x
	flake8 app --exclude=app/core/config.py
	mypy app
	black --check app --diff
	isort --recursive --check-only app

run_server_dev:
	uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload

run_server:
	gunicorn --bind 0.0.0.0:8000 app.main:app --workers ${GUINICORN_WORKERS} --timeout ${GUINICORN_TIME_OUT} -k uvicorn.workers.UvicornWorker

test:
	set -e
	set -x
	pytest -p no:warnings ./tests/*