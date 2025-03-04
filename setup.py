"""This module install prometheus-openstack-exporter."""

import os

from setuptools import setup


def read(fname):
    """Read a file and return the content."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="prometheus_openstack_exporter",
    version="0.0.4",
    author="Jacek Nykis",
    description="Exposes high level OpenStack metrics to Prometheus.",
    license="GPLv3",
    keywords=["prometheus", "openstack", "exporter"],
    url="https://github.com/CanonicalLtd/prometheus-openstack-exporter",
    scripts=["prometheus-openstack-exporter"],
    packages=[],
    install_requires=[
        "prometheus_client",
        "python-keystoneclient<=3.10.0",
        "python-novaclient==6.0.0",
        "python-neutronclient<=6.1.0",
        "python-cinderclient",
        "netaddr",
        "swift",
    ],
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: System :: Networking :: Monitoring",
        "License :: OSI Approved :: " "GNU General Public License v3 or later (GPLv3+)",
    ],
)
