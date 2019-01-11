PROJECTPATH = $(dir $(realpath $(firstword $(MAKEFILE_LIST))))
export GOPATH := $(PROJECTPATH)
export PATH := /usr/lib/go-1.11/bin:$(PATH)

VENV := .venv
VENV_PIP := $(PROJECTPATH)/$(VENV)/bin/pip
VENV_PYTHON := $(PROJECTPATH)/$(VENV)/bin/python2.7

EXTRA_PY := $(PROJECTPATH)/prometheus-openstack-exporter

FLAKE8 := $(VENV_PYTHON) -m flake8

all: lint test build

build:
	go install project/cmd/example

clean: clean-go clean-python clean-venv

clean-go:
	rm -rf $(PROJECTPATH)/bin
	rm -rf $(PROJECTPATH)/pkg

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
	    git-buildpackage \
	    golang-1.11  # Requires ppa:canonical-sysadmins/golang

lint: lint-go lint-python

lint-go:
	go fmt project/...
	go vet project/...

# See .flake8 for config options.
lint-python: $(VENV)
	$(FLAKE8) $(PROJECTPATH) $(EXTRA_PY)

test: test-go test-python

test-go:
	go test project/...

test-python: $(VENV)
	$(VENV_PYTHON) -m unittest discover tests

$(VENV):
	virtualenv --system-site-packages -p python2.7 $(PROJECTPATH)/$(VENV)
	$(VENV_PIP) install -I -r requirements.txt
