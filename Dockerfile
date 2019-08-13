FROM python:2.7-alpine

RUN \
    apk update && \
    apk --no-cache -q add build-base linux-headers libffi-dev openssl-dev python2-dev && \
    apk --no-cache -q add git gcc make autoconf automake libtool libxml2-dev libxslt-dev && \
    cd /tmp && git clone https://github.com/openstack/liberasurecode && \
    cd liberasurecode && ./autogen.sh && ./configure && make && make test && make install && \
    cd / && rm -rf /tmp/liberasurecode && \
    pip install -U pip && \
    pip install python-neutronclient python-novaclient python-keystoneclient python-cinderclient \
    prometheus-client requests pyyaml netaddr swift flake8

COPY prometheus-openstack-exporter /
COPY prometheus-openstack-exporter.sample.yaml /
COPY wrapper.sh /

EXPOSE 9183
ENTRYPOINT ["/bin/sh", "/wrapper.sh"]
