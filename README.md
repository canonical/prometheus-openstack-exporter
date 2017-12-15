# Prometheus OpenStack exporter

Exposes high level [OpenStack](http://www.openstack.org/) metrics to [Prometheus](https://prometheus.io/).


# Deployment

## Requirements

```
sudo apt-get install python-neutronclient python-novaclient python-keystoneclient python-netaddr python-cinderclient python-os-client-config
```

Install prometheus_client. On Ubuntu 16.04:
```
apt-get install python-prometheus-client
```

On Ubuntu 14.04:
```
pip install prometheus_client
```

## Installation

```
# Copy example config in place, edit to your needs
sudo cp prometheus-openstack-exporter.yaml /etc/prometheus/

## Upstart
# Install job
sudo cp prometheus-openstack-exporter.conf /etc/init

# Configure novarc location:
sudo sh -c 'echo "NOVARC=/path/to/admin-novarc">/etc/default/prometheus-openstack-exporter'

## Systemd
# Install job
sudo cp prometheus-openstack-exporter.service /etc/systemd/system/

# create novarc
sudo cat <<EOF > /etc/prometheus-openstack-exporter/admin.novarc
export OS_USERNAME=Admin
export OS_TENANT_NAME=admin
export OS_PASSWORD=XXXX
export OS_REGION_NAME=cloudname
export OS_AUTH_URL=http://XX.XX.XX.XX:35357/v2.0
EOF

# create default config location
sudo sh -c 'echo "CONFIG_FILE=/etc/prometheus-openstack-exporter/prometheus-openstack-exporter.yaml">/etc/default/prometheus-openstack-exporter'


# Start
sudo start prometheus-openstack-exporter
```

Or to run interactively:

```
. /path/to/admin-novarc
./prometheus-openstack-exporter prometheus-openstack-exporter.yaml

```

# Configuration

Configuration options are documented in prometheus-openstack-exporter.yaml shipped with this project

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

