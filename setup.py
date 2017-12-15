import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="prometheus_openstack_exporter",
    version="0.0.3",
    author="Jacek Nykis",
    description="Exposes high level OpenStack metrics to Prometheus.",
    license="GPLv3",
    keywords=["prometheus", "openstack", "exporter"],
    url="https://github.com/CanonicalLtd/prometheus-openstack-exporter",
    scripts=["prometheus-openstack-exporter"],
    install_requires=["prometheus_client",
                      "os-client-config",
                      "python-keystoneclient<=3.10.0",
                      "python-novaclient==6.0.0",
                      "python-neutronclient<=6.1.0",
                      "python-cinderclient",
                      "netaddr"],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: System :: Networking :: Monitoring",
        "License :: OSI Approved :: "
            "GNU General Public License v3 or later (GPLv3+)",
    ],
)
