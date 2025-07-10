# Prometheus OpenStack exporter

> [!NOTE]
> This charm is deprecated. Please use the new charm [openstack-exporter](https://charmhub.io/openstack-exporter) instead. It is integrate with [COS](https://charmhub.io/cos-lite) natively.

Exposes high level [OpenStack](http://www.openstack.org/) metrics to [Prometheus](https://prometheus.io/).

Data can be visualised using [Grafana](https://grafana.com/) and the [OpenStack Clouds Dashboard](https://grafana.com/dashboards/7924)

## Deployment

### Requirements

```
sudo apt-get install python-neutronclient python-novaclient python-keystoneclient python-netaddr python-cinderclient
```

Install prometheus_client. On Ubuntu 16.04:
```
apt-get install python-prometheus-client
```

On Ubuntu 14.04:
```
pip install prometheus_client
```

### Installation

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

Or use Docker Image:

```
# docker-compose.yml
version: '2.1'
services:
  ostackexporter:
    image: moghaddas/prom-openstack-exporter:latest
    # check this examle env file
    env_file:
      - ./admin.novarc.example
    restart: unless-stopped
    expose:
      - 9183
    ports:
      - 9183:9183

# docker run
docker run \
  -itd \
  --name prom_openstack_exporter \
  -p 9183:9183 \
  --env-file=$(pwd)/admin.novarc.example \
  --restart=unless-stopped \
  moghaddas/prom-openstack-exporter:latest

```

## Configuration

Configuration options are documented in prometheus-openstack-exporter.yaml shipped with this project

## FAQ

### Why are openstack_allocation_ratio values hardcoded?

There is no way to retrieve them using OpenStack API.

Alternative approach could be to hardcode those values in queries but this approach breaks when allocation ratios change.

### Why hardcode swift host list?

Same as above, there is no way to retrieve swift hosts using API.

### Why not write dedicated swift exporter?

Swift stats are included mainly because they are trivial to retrieve. If and when standalone swift exporter appears we can revisit this approach

### Why cache data?

We are aware that Prometheus best practise is to avoid caching. Unfortunately queries we need to run are very heavy and in bigger clouds can take minutes to execute. This is problematic not only because of delays but also because multiple servers scraping the exporter could have negative impact on the cloud performance

### How are Swift account metrics obtained?

Fairly simply!  Given a copy of the Swift rings (in fact, we just need
account.ring.gz) we can load this up and then ask it where particular
accounts are located in the cluster.  We assume that Swift is
replicating properly, pick a node at random, and ask it for the
account's statistics with an HTTP HEAD request, which it returns.

### How hard would it be to export Swift usage by container?

Sending a GET request to the account URL yields a list of containers
(probably paginated, so watch out for that!).  In order to write a
container-exporter, one could add some code to fetch a list of
containers from the account server, load up the container ring, and
then use container_ring.get_nodes(account, container) and HTTP HEAD on
one of the resulting nodes to get a containers' statistics, although
without some caching cleverness this will scale poorly.

## Known Issues
### EOFError by pickle.py

You should wait. It needs dump file to generate metrics
