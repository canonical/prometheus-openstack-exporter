FROM python:2.7.15-alpine3.8

RUN \
    apk update && \
    apk --no-cache -q add build-base linux-headers && \
    pip install python-neutronclient python-novaclient python-keystoneclient python-cinderclient \
    prometheus-client requests pyyaml netaddr

COPY prometheus-openstack-exporter /
COPY prometheus-openstack-exporter.sh /
COPY prometheus-openstack-exporter.sample.yaml /

ENTRYPOINT ["/bin/sh", "/prometheus-openstack-exporter.sh"]
