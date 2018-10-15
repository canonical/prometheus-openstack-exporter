#!/bin/sh

configFile=${configFile:-"/etc/prometheus/prometheus-openstack-exporter.yaml"}
listenPort=${listenPort:-9183}
cacheInterval=${cacheInterval:-300}
cacheFileName=${cacheFileName:-"/tmp/test"}
cloud=${cloud:-myCloud}
vcpuRatio=${vcpuRatio:-1.0}
ramRatio=${ramRatio:-1.0}
diskRatio=${diskRatio:-1.0}
schedulableInstanceRam=${schedulableInstanceRam:-4096}
schedulableInstanceVcpu=${schedulableInstanceVcpu:-2}
schedulableInstanceDisk=${schedulableInstanceDisk:-20}
useNovaVolumes=${useNovaVolumes:-True}

mkdir /etc/prometheus
cp prometheus-openstack-exporter.sample.yaml ${configFile}

sed -i "s|LISTEN_PORT|${listenPort}|g" 					${configFile}
sed -i "s|CACHE_INTERVAL|${cacheInterval}|g" 				${configFile}
sed -i "s|CACHE_FILE|${cacheFileName}|g" 				${configFile}
sed -i "s|CLOUD|${cloud}|g" 						${configFile}
sed -i "s|VCPU_RATIO|${vcpuRatio}|g" 					${configFile}
sed -i "s|RAM_RATIO|${ramRatio}|g" 					${configFile}
sed -i "s|DISK_RATIO|${diskRatio}|g" 					${configFile}
sed -i "s|SCHEDULABLE_INSTANCE_RAM|${schedulableInstanceRam}|g" 	${configFile}
sed -i "s|SCHEDULABLE_INSTANCE_VCPU|${schedulableInstanceVcpu}|g" 	${configFile}
sed -i "s|SCHEDULABLE_INSTANCE_DISK|${schedulableInstanceDisk}|g" 	${configFile}
sed -i "s|USE_NOVA_VOLUMES|${useNovaVolumes}|g" 			${configFile}

touch ${cacheFileName}
/prometheus-openstack-exporter ${configFile}

exit 0
