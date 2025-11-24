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

Nice, this is a kube-native apps. Let's see what we have inside.

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


