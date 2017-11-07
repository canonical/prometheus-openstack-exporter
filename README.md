# Prometheus OpenStack exporter

Exposes high level [OpenStack](http://www.openstack.org/) metrics to [Prometheus](https://prometheus.io/).


# Deployment


## Requirements

yum install -y gcc
yum install -y python
yum install -y python-devel
yum install -y python-pip

pip install python-openstackclient
pip install python-neutronclient
pip install prometheus_client



## Build docker container

docker build -t prometheus-openstack-exporter .

# Edit configuration

Example congfiguration in config/default.admin.example

# Start

docker run -d --env-file ./config/default.admin.example --restart=always -p 9183:9183 prometheus-openstack-exporter





# FAQ

## Why are openstack_allocation_ratio values hardcoded?

There is no way to retrieve them using OpenStack API.

Alternative approach could be to hardcode those values in queries but this approach breaks when allocation ratios change.

## Why hardcode swift host list?

Same as above, there is no way to retrieve swift hosts using API.

## Why not write dedicated swift exporter?

Swift stats are included mainly because they are trivial to retrieve. If and when standalone swift exporter appears we can revisit this approach

## Why cache data?

We are aware that Prometheus best practise is to avoid caching. Unfortunately queries we need to run are very heavy and in bigger clouds can take minutes to execute. This is problematic not only because of delays but also because multiple servers scraping the exporter could have negative impact on the cloud performance

