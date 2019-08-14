PROJECTPATH = $(dir $(realpath $(firstword $(MAKEFILE_LIST))))

VENV := .venv
VENV_PIP := $(PROJECTPATH)/$(VENV)/bin/pip
VENV_PYTHON := $(PROJECTPATH)/$(VENV)/bin/python2.7

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

lint: lint-python

# See .flake8 for config options.
lint-python: $(VENV)
	$(FLAKE8) $(PROJECTPATH) $(EXTRA_PY)

test: test-python

test-python: $(VENV)
	$(VENV_PYTHON) -m unittest discover tests

$(VENV):
	virtualenv --system-site-packages -p python2.7 $(PROJECTPATH)/$(VENV)
	$(VENV_PIP) install -I -r requirements.txt
