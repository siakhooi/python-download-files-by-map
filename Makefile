help:
clean:
	rm -rf dist target coverage sample download_files_by_map-0.1.0.tar.gz \
	.pytest_cache .tox .coverage tests/__pycache__ src/download_files_by_map/__pycache__
run:
	poetry run download-files-by-map tests/test-data/map1.json
build:
	scripts/set-version.sh
	poetry build
install:
	poetry install
flake8:
	poetry run flake8
update:
	poetry update
test:
	 poetry run pytest --capture=sys \
	 --junit-xml=coverage/test-results.xml \
	 --cov=download_files_by_map \
	 --cov-report term-missing  \
	 --cov-report xml:coverage/coverage.xml \
	 --cov-report html:coverage/coverage.html \
	 --cov-report lcov:coverage/coverage.info

all: clean install flake8 build tox-run

release:
	scripts/release.sh

tox-run:
	tox run
