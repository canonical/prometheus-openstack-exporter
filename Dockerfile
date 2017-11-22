FROM python:2
RUN mkdir /config
RUN mkdir /var/cache/prometheus-openstack-exporter

ADD ./config/default.yaml /config/
ADD ./prometheus-openstack-exporter /
ADD ./run /

RUN pip install python-openstackclient
RUN pip install python-neutronclient
RUN pip install prometheus_client

#yum install -y gcc
#yum install -y python
#yum install -y python-devel
#yum install -y python-pip

CMD ["/run"]
