PROJECTPATH = $(dir $(realpath $(firstword $(MAKEFILE_LIST))))

VENV := .venv
VENV_PIP := $(PROJECTPATH)/$(VENV)/bin/pip
VENV_PYTHON := $(PROJECTPATH)/$(VENV)/bin/python3.8

EXTRA_PY := $(PROJECTPATH)/prometheus-openstack-exporter

FLAKE8 := $(VENV_PYTHON) -m flake8

all: lint test build

clean: clean-python clean-venv

clean-python:
	rm -rf $(PROJECTPATH)/__pycache__

clean-venv:
	rm -rf $(PROJECTPATH)/$(VENV)

dch:
	gbp dch --debian-tag='%(version)s' -D bionic --git-log --first-parent

deb-src:
	debuild -S -sa -I.git

install-build-depends:
	sudo apt install \
	    debhelper \
	    git-buildpackage

lint:
	@echo "Running lint checks"
	@tox -e lint

black:
	@echo "Reformat files with black"
	@tox -e black

test: test-python

test-python: $(VENV)
	$(VENV_PYTHON) -m unittest discover tests

$(VENV):
	virtualenv --system-site-packages -p python3.8 $(PROJECTPATH)/$(VENV)
	$(VENV_PIP) install -I -r requirements.txt
