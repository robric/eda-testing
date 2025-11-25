# Testing EDA on WSL

## Installation (Windows Laptop)

Source mostly derived https://docs.eda.dev/25.4/software-install/non-production/wsl/ and related links + chatgpt :-)

### Zscaler skip

Deactivate Zscaler security for the EDA installation (too many issues with certs otherwise).

<img width="325" height="260" alt="image" src="https://github.com/user-attachments/assets/043d283d-0d84-4369-8817-021b517550fa" />

### Installation Steps

Prerequisites: make sure wsl version is greater than 2.5
```
PS C:\Users\xxxxxxxx> wsl --version
WSL version: 2.6.1.0
Kernel version: 6.6.87.2-1
WSLg version: 1.0.66
MSRDC version: 1.2.6353
Direct3D version: 1.611.1-81528511
DXCore version: 10.0.26100.1-240331-1435.ge-release
Windows version: 10.0.26100.6899
```

Installation
- Get the base containerlab image by downloading the .wsl file (I used the one from here https://github.com/srl-labs/wsl-containerlab/releases/tag/0.71.1-1.0 )
- Double-click on the .wsl file to install the distribution in wsl
- Connect to the image (wsl -d Containerlab) and type the following:
```
sudo apt-get update
sudo update-ca-certificates
git clone https://github.com/nokia-eda/playground
cd playground
export EXT_DOMAIN_NAME=localhost
make try-eda
```

After some time
```
[...]
--> INFO: The UI can be reached using:
          https://127.0.0.1:9443
          https://::1:9443
          https://172.18.0.1:9443
          https://172.17.0.1:9443
          https://172.19.124.218:9443
          https://10.255.255.254:9443
          https://fc00:f853:ccd:e793::1:9443
          https://C-5CG53743Q8.localdomain:9443
--> INFO: EDA is launched
```
And that's all !

## Overview

This is a kube-native app ! Let's see what we have inside.

```
clab@C-5CG53743Q8:~/playground$ docker ps --all
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS          PORTS                                                NAMES
1fcf2e760ac2   kindest/node:v1.33.1   "/usr/local/bin/entr…"   16 minutes ago   Up 16 minutes   127.0.0.1:39723->6443/tcp, 0.0.0.0:9443->32767/tcp   eda-demo-control-plane
clab@C-5CG53743Q8:~/playground$ docker exec -it 1fcf2e760ac2 bash
root@eda-demo-control-plane:/# kubectl get ns
NAME                 STATUS   AGE
cert-manager         Active   14m
default              Active   16m
eda                  Active   12m
eda-system           Active   15m
kube-node-lease      Active   16m
kube-public          Active   16m
kube-system          Active   16m
local-path-storage   Active   16m
metallb-system       Active   16m
root@eda-demo-control-plane:
root@eda-demo-control-plane:/# kubectl  get pods -A
NAMESPACE            NAME                                             READY   STATUS    RESTARTS   AGE
cert-manager         cert-manager-777c6f8ff4-rgmzs                    1/1     Running   0          17m
cert-manager         cert-manager-cainjector-6558fc6578-p7v2s         1/1     Running   0          17m
cert-manager         cert-manager-webhook-6964489477-d79q9            1/1     Running   0          17m
eda-system           cert-manager-csi-driver-bnvxk                    3/3     Running   0          16m
eda-system           cx-eda--leaf1-sim-7675894f69-vcq9x               2/2     Running   0          8m14s
eda-system           cx-eda--leaf2-sim-778f64c867-tzmbc               2/2     Running   0          8m9s
eda-system           cx-eda--spine1-sim-6b7f5f6db8-7xqr6              2/2     Running   0          8m9s
eda-system           cx-eda--testman-default-sim-78dc8b8495-nz7fh     2/2     Running   0          8m16s
eda-system           eda-api-fc65bd66c-dw74c                          1/1     Running   0          15m
eda-system           eda-appstore-96bccd846-wlmkf                     1/1     Running   0          15m
eda-system           eda-asvr-75c9d8d978-5xk7x                        1/1     Running   0          15m
eda-system           eda-bsvr-6d79d7d5cc-8jhnm                        1/1     Running   0          15m
eda-system           eda-ce-598f7bfb7d-wzjtc                          1/1     Running   0          15m
eda-system           eda-cert-checker-6b9b6f466b-6m7b5                1/1     Running   0          15m
eda-system           eda-cx-6bd94c6b46-7vzk6                          1/1     Running   0          15m
eda-system           eda-fe-747957d476-jflxd                          1/1     Running   0          15m
eda-system           eda-fluentbit-5fn65                              1/1     Running   0          17m
eda-system           eda-fluentd-9b78f4c9f-b6w5p                      1/1     Running   0          17m
eda-system           eda-git-7487f97b5f-lvplr                         1/1     Running   0          16m
eda-system           eda-git-replica-6799f7bccb-bbj8m                 1/1     Running   0          16m
eda-system           eda-keycloak-7597dcb964-ctprh                    1/1     Running   0          15m
eda-system           eda-metrics-server-788b466b77-hhknr              1/1     Running   0          15m
eda-system           eda-npp-0                                        1/1     Running   0          5m3s
eda-system           eda-npp-1                                        1/1     Running   0          4m33s
eda-system           eda-postgres-bb4c86cc9-d76b6                     1/1     Running   0          15m
eda-system           eda-sa-5f8c677f97-n6gcm                          1/1     Running   0          15m
eda-system           eda-sc-6778dbb78f-8mqx2                          1/1     Running   0          15m
eda-system           eda-se-559f8894d6-44qm5                          1/1     Running   0          15m
eda-system           eda-toolbox-76886bc564-npz76                     1/1     Running   0          15m
eda-system           trust-manager-849b644bdf-9ghst                   1/1     Running   0          16m
kube-system          coredns-674b8bbfcf-5t4st                         1/1     Running   0          18m
kube-system          coredns-674b8bbfcf-9sp2z                         1/1     Running   0          18m
kube-system          etcd-eda-demo-control-plane                      1/1     Running   0          18m
kube-system          kindnet-kjd7w                                    1/1     Running   0          18m
kube-system          kube-apiserver-eda-demo-control-plane            1/1     Running   0          18m
kube-system          kube-controller-manager-eda-demo-control-plane   1/1     Running   0          18m
kube-system          kube-proxy-c7fbh                                 1/1     Running   0          18m
kube-system          kube-scheduler-eda-demo-control-plane            1/1     Running   0          18m
local-path-storage   local-path-provisioner-7dc846544d-2r56c          1/1     Running   0          18m
metallb-system       controller-5cbffbc46b-vrk6n                      1/1     Running   0          18m
metallb-system       speaker-6prgv                                    1/1     Running   0          18m
root@eda-demo-control-plane:/#
```
So in summary:

We have classical kubernetes overlays (various ns):
 - **cert-manager**: certificate management
 - **metallb**: local Load balancer
 - **local-path-storage**: local storage (pv)

More interesting things in the eda-system namespace:
- **Simulators**
  - `cx-eda--leaf1-sim`, `cx-eda--leaf2-sim`, `cx-eda--spine1-sim`, `cx-eda--testman-default-sim`
  - *Role:* EDA provides a built-in CX engine (Digital Twin) for network simulation. Here we simulate leaf/spine nodes and test manager for fabric topology.
- **Core Services**
  - `eda-api`, `eda-appstore`, `eda-asvr`, `eda-bsvr`, `eda-ce`, `eda-fe`, `eda-sa`, `eda-sc`, `eda-se`
  - *Role:* PI, app store, and core EDA services for orchestration and automation.
- **Support Services**
  - `eda-postgres`, `eda-keycloak`, `eda-metrics-server`, `eda-toolbox`
  - *Role:* Database, authentication, metrics, and utility tools.
- **Logging**
  - `eda-fluentbit`, `eda-fluentd`
  - *Role:* Collect and forward logs for observability.
- **Git Integration**
  - `eda-git`, `eda-git-replica`
  - *Role:* Manage GitOps workflows and configuration repositories.
- **Cert & Trust**
  - `eda-cert-checker`, `trust-manager`
  - *Role:* Certificate validation and trust management.
- **NPP Nodes**
  - `eda-npp-0`, `eda-npp-1`
  - *Role:* **Node Provisioning Platform** agents for Zero-Touch Provisioning (ZTP). Push initial configs /bootstrap scripts to network devices, ConfigEngine, IP assignment, TLS profiles...

There are tons of crds ! This is really nice. 

```
root@eda-demo-control-plane:/# kubectl get crds
NAME                                                    CREATED AT
addresspools.metallb.io                                 2025-11-24T13:37:47Z
aggregateroutes.protocols.eda.nokia.com                 2025-11-24T13:47:34Z
alarms.core.eda.nokia.com                               2025-11-24T13:40:12Z
appinstallers.appstore.eda.nokia.com                    2025-11-24T13:40:12Z
artifacts.artifacts.eda.nokia.com                       2025-11-24T13:40:12Z
aspathsetdeployments.routingpolicies.eda.nokia.com      2025-11-24T13:47:20Z
aspathsets.routingpolicies.eda.nokia.com                2025-11-24T13:47:20Z
attachmentlookups.routing.eda.nokia.com                 2025-11-24T13:47:10Z
backends.aifabrics.eda.nokia.com                        2025-11-24T13:47:22Z
backendstates.aifabrics.eda.nokia.com                   2025-11-24T13:47:22Z
banners.siteinfo.eda.nokia.com                          2025-11-24T13:47:18Z
bannerstates.siteinfo.eda.nokia.com                     2025-11-24T13:47:18Z
bfdprofiles.metallb.io                                  2025-11-24T13:37:47Z
bgpadvertisements.metallb.io                            2025-11-24T13:37:47Z
bgpgroupdeployments.protocols.eda.nokia.com             2025-11-24T13:47:34Z
bgpgroups.protocols.eda.nokia.com                       2025-11-24T13:47:34Z
bgpgroupstates.protocols.eda.nokia.com                  2025-11-24T13:47:34Z
bgppeers.metallb.io                                     2025-11-24T13:37:47Z
bgppeers.protocols.eda.nokia.com                        2025-11-24T13:47:34Z
bgppeerstates.protocols.eda.nokia.com                   2025-11-24T13:47:34Z
breakouts.interfaces.eda.nokia.com                      2025-11-24T13:47:33Z
bridgedomaindeployments.services.eda.nokia.com          2025-11-24T13:47:14Z
bridgedomains.services.eda.nokia.com                    2025-11-24T13:47:15Z
bridgedomainstates.services.eda.nokia.com               2025-11-24T13:47:15Z
bridgeinterfaces.services.eda.nokia.com                 2025-11-24T13:47:15Z
bridgeinterfacestates.services.eda.nokia.com            2025-11-24T13:47:15Z
bundles.trust.cert-manager.io                           2025-11-24T13:39:24Z
catalogs.appstore.eda.nokia.com                         2025-11-24T13:40:12Z
certificatechecks.certcheck.eda.nokia.com               2025-11-24T13:40:57Z
certificaterequests.cert-manager.io                     2025-11-24T13:38:58Z
certificates.cert-manager.io                            2025-11-24T13:38:58Z
challenges.acme.cert-manager.io                         2025-11-24T13:38:58Z
chassis.components.eda.nokia.com                        2025-11-24T13:47:25Z
checkdefaultbgppeerss.protocols.eda.nokia.com           2025-11-24T13:47:34Z
checkinterfacess.interfaces.eda.nokia.com               2025-11-24T13:47:33Z
cliplugins.environment.eda.nokia.com                    2025-11-24T13:47:23Z
clusterdiscoveries.components.eda.nokia.com             2025-11-24T13:47:25Z
clusterissuers.cert-manager.io                          2025-11-24T13:38:58Z
clusterroles.core.eda.nokia.com                         2025-11-24T13:40:12Z
communities.metallb.io                                  2025-11-24T13:37:47Z
communitysetdeployments.routingpolicies.eda.nokia.com   2025-11-24T13:47:20Z
communitysets.routingpolicies.eda.nokia.com             2025-11-24T13:47:20Z
components.components.eda.nokia.com                     2025-11-24T13:47:25Z
configlets.config.eda.nokia.com                         2025-11-24T13:47:19Z
configletstates.config.eda.nokia.com                    2025-11-24T13:47:19Z
controlmodules.components.eda.nokia.com                 2025-11-24T13:47:25Z
controlplanefilters.filters.eda.nokia.com               2025-11-24T13:47:13Z
cpuoverlays.components.eda.nokia.com                    2025-11-24T13:47:25Z
cxclusters.cx.eda.nokia.com                             2025-11-24T13:40:12Z
defaultaggregateroutes.protocols.eda.nokia.com          2025-11-24T13:47:34Z
defaultbgpgroupdeployments.protocols.eda.nokia.com      2025-11-24T13:47:34Z
defaultbgpgroups.protocols.eda.nokia.com                2025-11-24T13:47:34Z
defaultbgppeers.protocols.eda.nokia.com                 2025-11-24T13:47:34Z
defaultinterfaces.routing.eda.nokia.com                 2025-11-24T13:47:10Z
defaultinterfacestates.routing.eda.nokia.com            2025-11-24T13:47:10Z
defaultroutereflectorclients.protocols.eda.nokia.com    2025-11-24T13:47:34Z
defaultroutereflectors.protocols.eda.nokia.com          2025-11-24T13:47:34Z
defaultrouters.routing.eda.nokia.com                    2025-11-24T13:47:10Z
defaultrouterstates.routing.eda.nokia.com               2025-11-24T13:47:10Z
defaultstaticroutes.protocols.eda.nokia.com             2025-11-24T13:47:34Z
deployimages.os.eda.nokia.com                           2025-11-24T13:47:32Z
designers.core.eda.nokia.com                            2025-11-24T13:40:12Z
deviationactions.core.eda.nokia.com                     2025-11-24T13:40:12Z
deviationoverlays.topologies.eda.nokia.com              2025-11-24T13:47:29Z
deviations.core.eda.nokia.com                           2025-11-24T13:40:12Z
dhcprelays.services.eda.nokia.com                       2025-11-24T13:47:15Z
discoveries.components.eda.nokia.com                    2025-11-24T13:47:25Z
discoveryaggregatestates.components.eda.nokia.com       2025-11-24T13:47:25Z
discoverystates.components.eda.nokia.com                2025-11-24T13:47:25Z
drains.routing.eda.nokia.com                            2025-11-24T13:47:10Z
drainstates.routing.eda.nokia.com                       2025-11-24T13:47:10Z
edgeinterfaces.core.eda.nokia.com                       2025-11-24T13:40:12Z
edgepings.services.eda.nokia.com                        2025-11-24T13:47:15Z
egresspolicys.qos.eda.nokia.com                         2025-11-24T13:47:24Z
engineconfigs.core.eda.nokia.com                        2025-11-24T13:40:12Z
fabricmodules.components.eda.nokia.com                  2025-11-24T13:47:25Z
fabrics.fabrics.eda.nokia.com                           2025-11-24T13:47:27Z
fabricstates.fabrics.eda.nokia.com                      2025-11-24T13:47:27Z
fans.components.eda.nokia.com                           2025-11-24T13:47:25Z
filterdeployments.filters.eda.nokia.com                 2025-11-24T13:47:13Z
filters.filters.eda.nokia.com                           2025-11-24T13:47:13Z
forwardingclasss.qos.eda.nokia.com                      2025-11-24T13:47:24Z
globalconfigs.core.eda.nokia.com                        2025-11-24T13:40:12Z
httpproxies.core.eda.nokia.com                          2025-11-24T13:40:12Z
indexallocationpools.core.eda.nokia.com                 2025-11-24T13:40:12Z
ingresspolicys.qos.eda.nokia.com                        2025-11-24T13:47:24Z
inits.bootstrap.eda.nokia.com                           2025-11-24T13:47:17Z
interfacemodules.components.eda.nokia.com               2025-11-24T13:47:25Z
interfaces.interfaces.eda.nokia.com                     2025-11-24T13:47:33Z
interfacestates.interfaces.eda.nokia.com                2025-11-24T13:47:33Z
ipaddresspools.metallb.io                               2025-11-24T13:37:47Z
ipallocationpools.core.eda.nokia.com                    2025-11-24T13:40:12Z
ipinsubnetallocationpools.core.eda.nokia.com            2025-11-24T13:40:12Z
irbinterfaces.services.eda.nokia.com                    2025-11-24T13:47:14Z
irbinterfacestates.services.eda.nokia.com               2025-11-24T13:47:15Z
islpings.fabrics.eda.nokia.com                          2025-11-24T13:47:27Z
isls.fabrics.eda.nokia.com                              2025-11-24T13:47:27Z
islstates.fabrics.eda.nokia.com                         2025-11-24T13:47:27Z
issuers.cert-manager.io                                 2025-11-24T13:38:58Z
keychaindeployments.security.eda.nokia.com              2025-11-24T13:47:12Z
keychains.security.eda.nokia.com                        2025-11-24T13:47:12Z
l2advertisements.metallb.io                             2025-11-24T13:37:47Z
licenses.core.eda.nokia.com                             2025-11-24T13:40:12Z
lldpoverlays.topologies.eda.nokia.com                   2025-11-24T13:47:29Z
managementrouters.bootstrap.eda.nokia.com               2025-11-24T13:47:17Z
managementrouterstates.bootstrap.eda.nokia.com          2025-11-24T13:47:17Z
manifests.core.eda.nokia.com                            2025-11-24T13:40:12Z
memoryoverlays.components.eda.nokia.com                 2025-11-24T13:47:25Z
mirrorfilterdeployments.filters.eda.nokia.com           2025-11-24T13:47:13Z
mirrorfilters.filters.eda.nokia.com                     2025-11-24T13:47:13Z
mirrors.oam.eda.nokia.com                               2025-11-24T13:47:28Z
mirrorstates.oam.eda.nokia.com                          2025-11-24T13:47:28Z
monitoraggregatestates.components.eda.nokia.com         2025-11-24T13:47:25Z
monitoraggregatestates.system.eda.nokia.com             2025-11-24T13:47:31Z
monitors.components.eda.nokia.com                       2025-11-24T13:47:25Z
monitors.system.eda.nokia.com                           2025-11-24T13:47:31Z
monitorstates.components.eda.nokia.com                  2025-11-24T13:47:25Z
monitorstates.system.eda.nokia.com                      2025-11-24T13:47:31Z
namespaces.core.eda.nokia.com                           2025-11-24T13:40:12Z
nodeconfigs.core.eda.nokia.com                          2025-11-24T13:40:12Z
nodegroupdeployments.aaa.eda.nokia.com                  2025-11-24T13:47:32Z
nodegroups.aaa.eda.nokia.com                            2025-11-24T13:47:32Z
nodeprofiles.core.eda.nokia.com                         2025-11-24T13:40:13Z
nodesecurityprofiles.core.eda.nokia.com                 2025-11-24T13:40:13Z
nodeusers.core.eda.nokia.com                            2025-11-24T13:40:13Z
nodeuserstates.aaa.eda.nokia.com                        2025-11-24T13:47:32Z
ntpclients.timing.eda.nokia.com                         2025-11-24T13:47:09Z
ntpclientstates.timing.eda.nokia.com                    2025-11-24T13:47:09Z
orders.acme.cert-manager.io                             2025-11-24T13:38:58Z
pings.oam.eda.nokia.com                                 2025-11-24T13:47:28Z
policyattachments.qos.eda.nokia.com                     2025-11-24T13:47:24Z
policydeployments.qos.eda.nokia.com                     2025-11-24T13:47:24Z
policydeployments.routingpolicies.eda.nokia.com         2025-11-24T13:47:20Z
policys.routingpolicies.eda.nokia.com                   2025-11-24T13:47:20Z
powersupplies.components.eda.nokia.com                  2025-11-24T13:47:25Z
prefixsetdeployments.routingpolicies.eda.nokia.com      2025-11-24T13:47:20Z
prefixsets.routingpolicies.eda.nokia.com                2025-11-24T13:47:20Z
queues.qos.eda.nokia.com                                2025-11-24T13:47:24Z
registries.appstore.eda.nokia.com                       2025-11-24T13:40:13Z
resourcegroups.kpt.dev                                  2025-11-24T13:38:31Z
roles.core.eda.nokia.com                                2025-11-24T13:40:13Z
routedinterfaces.services.eda.nokia.com                 2025-11-24T13:47:15Z
routedinterfacestates.services.eda.nokia.com            2025-11-24T13:47:14Z
routelookups.routing.eda.nokia.com                      2025-11-24T13:47:10Z
routerdeployments.services.eda.nokia.com                2025-11-24T13:47:14Z
routereflectorclients.protocols.eda.nokia.com           2025-11-24T13:47:34Z
routereflectorclientstates.protocols.eda.nokia.com      2025-11-24T13:47:34Z
routereflectors.protocols.eda.nokia.com                 2025-11-24T13:47:34Z
routereflectorstates.protocols.eda.nokia.com            2025-11-24T13:47:34Z
routers.services.eda.nokia.com                          2025-11-24T13:47:15Z
routerstates.services.eda.nokia.com                     2025-11-24T13:47:15Z
setupenvs.environment.eda.nokia.com                     2025-11-24T13:47:23Z
simlinks.core.eda.nokia.com                             2025-11-24T13:40:13Z
simnodes.core.eda.nokia.com                             2025-11-24T13:40:13Z
stateconfigs.services.eda.nokia.com                     2025-11-24T13:47:15Z
staticroutes.protocols.eda.nokia.com                    2025-11-24T13:47:34Z
subnetallocationpools.core.eda.nokia.com                2025-11-24T13:40:13Z
systeminterfaces.routing.eda.nokia.com                  2025-11-24T13:47:10Z
systeminterfacestates.routing.eda.nokia.com             2025-11-24T13:47:10Z
targetnodes.core.eda.nokia.com                          2025-11-24T13:40:13Z
techsupports.oam.eda.nokia.com                          2025-11-24T13:47:28Z
thresholds.oam.eda.nokia.com                            2025-11-24T13:47:28Z
thresholds.platformmetrics.eda.nokia.com                2025-11-24T13:40:13Z
topobreakouts.core.eda.nokia.com                        2025-11-24T13:40:13Z
topolinkmonitors.topologies.eda.nokia.com               2025-11-24T13:47:29Z
topolinks.core.eda.nokia.com                            2025-11-24T13:40:13Z
topolinkstates.topologies.eda.nokia.com                 2025-11-24T13:47:29Z
topologies.topologies.eda.nokia.com                     2025-11-24T13:47:29Z
topologygroupings.topologies.eda.nokia.com              2025-11-24T13:47:29Z
toponodes.core.eda.nokia.com                            2025-11-24T13:40:13Z
trafficrateoverlays.topologies.eda.nokia.com            2025-11-24T13:47:29Z
transactionresults.core.eda.nokia.com                   2025-11-24T13:40:13Z
transactions.core.eda.nokia.com                         2025-11-24T13:40:14Z
udpproxies.core.eda.nokia.com                           2025-11-24T13:40:14Z
userdeployments.aaa.eda.nokia.com                       2025-11-24T13:47:32Z
virtualnetworks.services.eda.nokia.com                  2025-11-24T13:47:15Z
virtualnetworkstates.services.eda.nokia.com             2025-11-24T13:47:15Z
vlans.services.eda.nokia.com                            2025-11-24T13:47:15Z
vlanstates.services.eda.nokia.com                       2025-11-24T13:47:14Z
volumeoverlays.components.eda.nokia.com                 2025-11-24T13:47:25Z
waitforinputs.core.eda.nokia.com                        2025-11-24T13:40:14Z
workflowdefinitions.core.eda.nokia.com                  2025-11-24T13:40:14Z
workflows.core.eda.nokia.com                            2025-11-24T13:40:14Z
root@eda-demo-control-plane:/# kubectl get crds | grep nokia
aggregateroutes.protocols.eda.nokia.com                 2025-11-24T13:47:34Z
alarms.core.eda.nokia.com                               2025-11-24T13:40:12Z
appinstallers.appstore.eda.nokia.com                    2025-11-24T13:40:12Z
artifacts.artifacts.eda.nokia.com                       2025-11-24T13:40:12Z
aspathsetdeployments.routingpolicies.eda.nokia.com      2025-11-24T13:47:20Z
aspathsets.routingpolicies.eda.nokia.com                2025-11-24T13:47:20Z
attachmentlookups.routing.eda.nokia.com                 2025-11-24T13:47:10Z
backends.aifabrics.eda.nokia.com                        2025-11-24T13:47:22Z
backendstates.aifabrics.eda.nokia.com                   2025-11-24T13:47:22Z
banners.siteinfo.eda.nokia.com                          2025-11-24T13:47:18Z
bannerstates.siteinfo.eda.nokia.com                     2025-11-24T13:47:18Z
bgpgroupdeployments.protocols.eda.nokia.com             2025-11-24T13:47:34Z
bgpgroups.protocols.eda.nokia.com                       2025-11-24T13:47:34Z
bgpgroupstates.protocols.eda.nokia.com                  2025-11-24T13:47:34Z
bgppeers.protocols.eda.nokia.com                        2025-11-24T13:47:34Z
bgppeerstates.protocols.eda.nokia.com                   2025-11-24T13:47:34Z
breakouts.interfaces.eda.nokia.com                      2025-11-24T13:47:33Z
bridgedomaindeployments.services.eda.nokia.com          2025-11-24T13:47:14Z
bridgedomains.services.eda.nokia.com                    2025-11-24T13:47:15Z
bridgedomainstates.services.eda.nokia.com               2025-11-24T13:47:15Z
bridgeinterfaces.services.eda.nokia.com                 2025-11-24T13:47:15Z
bridgeinterfacestates.services.eda.nokia.com            2025-11-24T13:47:15Z
catalogs.appstore.eda.nokia.com                         2025-11-24T13:40:12Z
certificatechecks.certcheck.eda.nokia.com               2025-11-24T13:40:57Z
chassis.components.eda.nokia.com                        2025-11-24T13:47:25Z
checkdefaultbgppeerss.protocols.eda.nokia.com           2025-11-24T13:47:34Z
checkinterfacess.interfaces.eda.nokia.com               2025-11-24T13:47:33Z
cliplugins.environment.eda.nokia.com                    2025-11-24T13:47:23Z
clusterdiscoveries.components.eda.nokia.com             2025-11-24T13:47:25Z
clusterroles.core.eda.nokia.com                         2025-11-24T13:40:12Z
communitysetdeployments.routingpolicies.eda.nokia.com   2025-11-24T13:47:20Z
communitysets.routingpolicies.eda.nokia.com             2025-11-24T13:47:20Z
components.components.eda.nokia.com                     2025-11-24T13:47:25Z
configlets.config.eda.nokia.com                         2025-11-24T13:47:19Z
configletstates.config.eda.nokia.com                    2025-11-24T13:47:19Z
controlmodules.components.eda.nokia.com                 2025-11-24T13:47:25Z
controlplanefilters.filters.eda.nokia.com               2025-11-24T13:47:13Z
cpuoverlays.components.eda.nokia.com                    2025-11-24T13:47:25Z
cxclusters.cx.eda.nokia.com                             2025-11-24T13:40:12Z
defaultaggregateroutes.protocols.eda.nokia.com          2025-11-24T13:47:34Z
defaultbgpgroupdeployments.protocols.eda.nokia.com      2025-11-24T13:47:34Z
defaultbgpgroups.protocols.eda.nokia.com                2025-11-24T13:47:34Z
defaultbgppeers.protocols.eda.nokia.com                 2025-11-24T13:47:34Z
defaultinterfaces.routing.eda.nokia.com                 2025-11-24T13:47:10Z
defaultinterfacestates.routing.eda.nokia.com            2025-11-24T13:47:10Z
defaultroutereflectorclients.protocols.eda.nokia.com    2025-11-24T13:47:34Z
defaultroutereflectors.protocols.eda.nokia.com          2025-11-24T13:47:34Z
defaultrouters.routing.eda.nokia.com                    2025-11-24T13:47:10Z
defaultrouterstates.routing.eda.nokia.com               2025-11-24T13:47:10Z
defaultstaticroutes.protocols.eda.nokia.com             2025-11-24T13:47:34Z
deployimages.os.eda.nokia.com                           2025-11-24T13:47:32Z
designers.core.eda.nokia.com                            2025-11-24T13:40:12Z
deviationactions.core.eda.nokia.com                     2025-11-24T13:40:12Z
deviationoverlays.topologies.eda.nokia.com              2025-11-24T13:47:29Z
deviations.core.eda.nokia.com                           2025-11-24T13:40:12Z
dhcprelays.services.eda.nokia.com                       2025-11-24T13:47:15Z
discoveries.components.eda.nokia.com                    2025-11-24T13:47:25Z
discoveryaggregatestates.components.eda.nokia.com       2025-11-24T13:47:25Z
discoverystates.components.eda.nokia.com                2025-11-24T13:47:25Z
drains.routing.eda.nokia.com                            2025-11-24T13:47:10Z
drainstates.routing.eda.nokia.com                       2025-11-24T13:47:10Z
edgeinterfaces.core.eda.nokia.com                       2025-11-24T13:40:12Z
edgepings.services.eda.nokia.com                        2025-11-24T13:47:15Z
egresspolicys.qos.eda.nokia.com                         2025-11-24T13:47:24Z
engineconfigs.core.eda.nokia.com                        2025-11-24T13:40:12Z
fabricmodules.components.eda.nokia.com                  2025-11-24T13:47:25Z
fabrics.fabrics.eda.nokia.com                           2025-11-24T13:47:27Z
fabricstates.fabrics.eda.nokia.com                      2025-11-24T13:47:27Z
fans.components.eda.nokia.com                           2025-11-24T13:47:25Z
filterdeployments.filters.eda.nokia.com                 2025-11-24T13:47:13Z
filters.filters.eda.nokia.com                           2025-11-24T13:47:13Z
forwardingclasss.qos.eda.nokia.com                      2025-11-24T13:47:24Z
globalconfigs.core.eda.nokia.com                        2025-11-24T13:40:12Z
httpproxies.core.eda.nokia.com                          2025-11-24T13:40:12Z
indexallocationpools.core.eda.nokia.com                 2025-11-24T13:40:12Z
ingresspolicys.qos.eda.nokia.com                        2025-11-24T13:47:24Z
inits.bootstrap.eda.nokia.com                           2025-11-24T13:47:17Z
interfacemodules.components.eda.nokia.com               2025-11-24T13:47:25Z
interfaces.interfaces.eda.nokia.com                     2025-11-24T13:47:33Z
interfacestates.interfaces.eda.nokia.com                2025-11-24T13:47:33Z
ipallocationpools.core.eda.nokia.com                    2025-11-24T13:40:12Z
ipinsubnetallocationpools.core.eda.nokia.com            2025-11-24T13:40:12Z
irbinterfaces.services.eda.nokia.com                    2025-11-24T13:47:14Z
irbinterfacestates.services.eda.nokia.com               2025-11-24T13:47:15Z
islpings.fabrics.eda.nokia.com                          2025-11-24T13:47:27Z
isls.fabrics.eda.nokia.com                              2025-11-24T13:47:27Z
islstates.fabrics.eda.nokia.com                         2025-11-24T13:47:27Z
keychaindeployments.security.eda.nokia.com              2025-11-24T13:47:12Z
keychains.security.eda.nokia.com                        2025-11-24T13:47:12Z
licenses.core.eda.nokia.com                             2025-11-24T13:40:12Z
lldpoverlays.topologies.eda.nokia.com                   2025-11-24T13:47:29Z
managementrouters.bootstrap.eda.nokia.com               2025-11-24T13:47:17Z
managementrouterstates.bootstrap.eda.nokia.com          2025-11-24T13:47:17Z
manifests.core.eda.nokia.com                            2025-11-24T13:40:12Z
memoryoverlays.components.eda.nokia.com                 2025-11-24T13:47:25Z
mirrorfilterdeployments.filters.eda.nokia.com           2025-11-24T13:47:13Z
mirrorfilters.filters.eda.nokia.com                     2025-11-24T13:47:13Z
mirrors.oam.eda.nokia.com                               2025-11-24T13:47:28Z
mirrorstates.oam.eda.nokia.com                          2025-11-24T13:47:28Z
monitoraggregatestates.components.eda.nokia.com         2025-11-24T13:47:25Z
monitoraggregatestates.system.eda.nokia.com             2025-11-24T13:47:31Z
monitors.components.eda.nokia.com                       2025-11-24T13:47:25Z
monitors.system.eda.nokia.com                           2025-11-24T13:47:31Z
monitorstates.components.eda.nokia.com                  2025-11-24T13:47:25Z
monitorstates.system.eda.nokia.com                      2025-11-24T13:47:31Z
namespaces.core.eda.nokia.com                           2025-11-24T13:40:12Z
nodeconfigs.core.eda.nokia.com                          2025-11-24T13:40:12Z
nodegroupdeployments.aaa.eda.nokia.com                  2025-11-24T13:47:32Z
nodegroups.aaa.eda.nokia.com                            2025-11-24T13:47:32Z
nodeprofiles.core.eda.nokia.com                         2025-11-24T13:40:13Z
nodesecurityprofiles.core.eda.nokia.com                 2025-11-24T13:40:13Z
nodeusers.core.eda.nokia.com                            2025-11-24T13:40:13Z
nodeuserstates.aaa.eda.nokia.com                        2025-11-24T13:47:32Z
ntpclients.timing.eda.nokia.com                         2025-11-24T13:47:09Z
ntpclientstates.timing.eda.nokia.com                    2025-11-24T13:47:09Z
pings.oam.eda.nokia.com                                 2025-11-24T13:47:28Z
policyattachments.qos.eda.nokia.com                     2025-11-24T13:47:24Z
policydeployments.qos.eda.nokia.com                     2025-11-24T13:47:24Z
policydeployments.routingpolicies.eda.nokia.com         2025-11-24T13:47:20Z
policys.routingpolicies.eda.nokia.com                   2025-11-24T13:47:20Z
powersupplies.components.eda.nokia.com                  2025-11-24T13:47:25Z
prefixsetdeployments.routingpolicies.eda.nokia.com      2025-11-24T13:47:20Z
prefixsets.routingpolicies.eda.nokia.com                2025-11-24T13:47:20Z
queues.qos.eda.nokia.com                                2025-11-24T13:47:24Z
registries.appstore.eda.nokia.com                       2025-11-24T13:40:13Z
roles.core.eda.nokia.com                                2025-11-24T13:40:13Z
routedinterfaces.services.eda.nokia.com                 2025-11-24T13:47:15Z
routedinterfacestates.services.eda.nokia.com            2025-11-24T13:47:14Z
routelookups.routing.eda.nokia.com                      2025-11-24T13:47:10Z
routerdeployments.services.eda.nokia.com                2025-11-24T13:47:14Z
routereflectorclients.protocols.eda.nokia.com           2025-11-24T13:47:34Z
routereflectorclientstates.protocols.eda.nokia.com      2025-11-24T13:47:34Z
routereflectors.protocols.eda.nokia.com                 2025-11-24T13:47:34Z
routereflectorstates.protocols.eda.nokia.com            2025-11-24T13:47:34Z
routers.services.eda.nokia.com                          2025-11-24T13:47:15Z
routerstates.services.eda.nokia.com                     2025-11-24T13:47:15Z
setupenvs.environment.eda.nokia.com                     2025-11-24T13:47:23Z
simlinks.core.eda.nokia.com                             2025-11-24T13:40:13Z
simnodes.core.eda.nokia.com                             2025-11-24T13:40:13Z
stateconfigs.services.eda.nokia.com                     2025-11-24T13:47:15Z
staticroutes.protocols.eda.nokia.com                    2025-11-24T13:47:34Z
subnetallocationpools.core.eda.nokia.com                2025-11-24T13:40:13Z
systeminterfaces.routing.eda.nokia.com                  2025-11-24T13:47:10Z
systeminterfacestates.routing.eda.nokia.com             2025-11-24T13:47:10Z
targetnodes.core.eda.nokia.com                          2025-11-24T13:40:13Z
techsupports.oam.eda.nokia.com                          2025-11-24T13:47:28Z
thresholds.oam.eda.nokia.com                            2025-11-24T13:47:28Z
thresholds.platformmetrics.eda.nokia.com                2025-11-24T13:40:13Z
topobreakouts.core.eda.nokia.com                        2025-11-24T13:40:13Z
topolinkmonitors.topologies.eda.nokia.com               2025-11-24T13:47:29Z
topolinks.core.eda.nokia.com                            2025-11-24T13:40:13Z
topolinkstates.topologies.eda.nokia.com                 2025-11-24T13:47:29Z
topologies.topologies.eda.nokia.com                     2025-11-24T13:47:29Z
topologygroupings.topologies.eda.nokia.com              2025-11-24T13:47:29Z
toponodes.core.eda.nokia.com                            2025-11-24T13:40:13Z
trafficrateoverlays.topologies.eda.nokia.com            2025-11-24T13:47:29Z
transactionresults.core.eda.nokia.com                   2025-11-24T13:40:13Z
transactions.core.eda.nokia.com                         2025-11-24T13:40:14Z
udpproxies.core.eda.nokia.com                           2025-11-24T13:40:14Z
userdeployments.aaa.eda.nokia.com                       2025-11-24T13:47:32Z
virtualnetworks.services.eda.nokia.com                  2025-11-24T13:47:15Z
virtualnetworkstates.services.eda.nokia.com             2025-11-24T13:47:15Z
vlans.services.eda.nokia.com                            2025-11-24T13:47:15Z
vlanstates.services.eda.nokia.com                       2025-11-24T13:47:14Z
volumeoverlays.components.eda.nokia.com                 2025-11-24T13:47:25Z
waitforinputs.core.eda.nokia.com                        2025-11-24T13:40:14Z
workflowdefinitions.core.eda.nokia.com                  2025-11-24T13:40:14Z
workflows.core.eda.nokia.com                            2025-11-24T13:40:14Z
root@eda-demo-control-plane:/#
root@eda-demo-control-plane:/# kubectl get crds | grep nokia | wc
    168     336   12936
root@eda-demo-control-plane:/#


```
### Testing 

1. Load topology (make script)

The demo topology can be pre-loaded via make. This populates the eda-topology config map with node and links.

<img width="836" height="454" alt="image" src="https://github.com/user-attachments/assets/b841d8db-33c0-4aef-af1a-7e462c3b2aff" />

```
clab@C-5CG53743Q8:~/playground$ make topology-load
--> TOPO: JSON Processing
configmap/eda-topology configured
configmap/eda-topology-sim unchanged
--> TOPO: config created in cluster
--> TOPO: Using POD_NAME: eda-api-fc65bd66c-dw74c
--> TOPO: Checking if eda-api-fc65bd66c-dw74c is Running
[...]
root@eda-demo-control-plane:/# kubectl get -n eda cm eda-topology -o yaml
apiVersion: v1
data:
  eda.yaml: |
    ---
    items:
      - spec:
          nodes:
            - name: leaf1
              labels:
                eda.nokia.com/role: leaf
                eda.nokia.com/security-profile: managed
              spec:
                operatingSystem: srl
                version: 25.7.2
                platform: 7220 IXR-D3L
                nodeProfile: srlinux-ghcr-25.7.2
[...]
          links:
            - name: leaf1-spine1-1
              labels:
                eda.nokia.com/role: interSwitch
              spec:
                links:
                  - local:
                      node: leaf1
                      interface: ethernet-1-1
                    remote:
                      node: spine1
                      interface: ethernet-1-1
                    type: interSwitch
[...]

```

Check the nodes. Note that NPP is disconnected. This is not good. I tried many things, but couldn't spot the issue (looks like npp can't reach CX switches ? might be TLS-related  ?) .

```
root@eda-demo-control-plane:/# kubectl get -n eda toponodes
NAME     PLATFORM       VERSION   OS    ONBOARDED   MODE     NPP            NODE   AGE
leaf1    7220 IXR-D3L   25.7.2    srl   true        normal   Disconnected          141m
leaf2    7220 IXR-D3L   25.7.2    srl   true        normal   Disconnected          141m
spine1   7220 IXR-D5    25.7.2    srl   true        normal   Disconnected          141m
root@eda-demo-control-plane:/#
root@eda-demo-control-plane:/# kubectl get -n eda topolinks
NAME                 AGE
leaf1-2-e1212        145m
leaf1-e1011          145m
leaf1-ethernet-1-3   145m
leaf1-ethernet-1-4   145m
leaf1-ethernet-1-5   145m
leaf1-ethernet-1-6   145m
leaf1-ethernet-1-7   145m
leaf1-ethernet-1-8   145m
leaf1-ethernet-1-9   145m
leaf1-spine1-1       145m
leaf1-spine1-2       145m
leaf2-e1011          145m
leaf2-ethernet-1-3   145m
leaf2-ethernet-1-4   145m
leaf2-ethernet-1-5   145m
leaf2-ethernet-1-6   145m
leaf2-ethernet-1-7   145m
leaf2-ethernet-1-8   145m
leaf2-ethernet-1-9   145m
leaf2-spine1-1       145m
leaf2-spine1-2       145m
root@eda-demo-control-plane:/# k
```

OK something went wrong ( probably messed up with reactivating zscaler security too early ?). Let's restart the install:

```
make teardown-cluster
rm -rf eda-kpt
export EXT_DOMAIN_NAME=localhost
make try-eda
```

Now it works !

```
root@eda-demo-control-plane:/# kubectl get toponodes -A
NAMESPACE   NAME     PLATFORM       VERSION   OS    ONBOARDED   MODE     NPP         NODE     AGE
eda         leaf1    7220 IXR-D3L   25.7.2    srl   true        normal   Connected   Synced   4m34s
eda         leaf2    7220 IXR-D3L   25.7.2    srl   true        normal   Connected   Synced   4m34s
eda         spine1   7220 IXR-D5    25.7.2    srl   true        normal   Connected   Synced   4m34s
root@eda-demo-control-plane:/# 
```

You can connect to cli of the emulated devices from k8s (admin/NokiaSrl1!).

```
root@eda-demo-control-plane:/# kubectl get pods -A| grep sim
eda-system           cx-eda--leaf1-sim-65bcb67766-fwjcm               2/2     Running   0          75m
eda-system           cx-eda--leaf2-sim-74645ff576-q76cv               2/2     Running   0          75m
eda-system           cx-eda--spine1-sim-ccd9976f-t75kr                2/2     Running   0          75m
eda-system           cx-eda--testman-default-sim-78dc8b8495-csj5l     2/2     Running   0          75m
root@eda-demo-control-plane:/#

root@eda-demo-control-plane:/# kubectl exec -it cx-eda--leaf1-sim-65bcb67766-fwjcm -n eda-system -- ssh admin@localhost
Defaulted container "leaf1" out of: leaf1, cxdp
admin@localhost's password:
Last login: Tue Nov 25 12:02:10 2025 from ::1


Loading environment configuration file(s): ['/etc/opt/srlinux/srlinux.rc']
Welcome to the Nokia SR Linux CLI.

--{ + running }--[  ]--
A:admin@leaf1#
```

