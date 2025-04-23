help:
clean:
	rm -rf dist target coverage sample
run:
	poetry run download-files-by-map map-sample.json
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

all: clean install flake8 build test

release:
	scripts/release.sh

commit:
	scripts/git-commit.sh
