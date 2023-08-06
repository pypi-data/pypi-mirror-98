#!/usr/bin/env make

PACKAGE_NAME="atudomain_git"
GREEN='\033[0;32m'
NC='\033[0m'

.PHONY : venv
venv:
	virtualenv venv
	@echo ""
	@echo "${GREEN}Run 'source venv/bin/activate' to activate venv${NC}"

clean-venv:
	rm -rf venv

clean:
	find . -name "*.pyc" -delete
	rm -rf dist docs/build build ${PACKAGE_NAME}.egg-info .eggs .pytest_cache

install:
	python3 -m pip install .

uninstall:
	python3 -m pip uninstall -y ${PACKAGE_NAME}

package: dist docs

dist: test
	python3 setup.py sdist bdist_wheel

test:
	python3 setup.py test

tox:
	tox

.PHONY : docs
docs:
	python3 setup.py build_sphinx

release-patch:
	bumpversion patch

release-minor:
	bumpversion minor

release-major:
	bumpversion major

upload:
	rm -f dist/*
	@echo "${GREEN}INFO:	Upload package to pypi.python.org${NC}"
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
