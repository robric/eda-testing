# Testing EDA on WSL

## Installation (Nokia Windows Laptop)

Source mostly derived https://docs.eda.dev/25.4/software-install/non-production/wsl/ and related links + chatgpt :-)

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
- Connect to the image (wsl -d Containerlab)
- There are some issues with certificates of the WSL image. Zscaler is a "painful man in the middle". First export the Zscaler certificate from Windows. Launch the "Manage User Certificates" from windows and export the Zscaler Root certificate to a base64-encrypted file (here called zscaler-ca.cer).
<img width="618" height="439" alt="image" src="https://github.com/user-attachments/assets/19112c57-d072-47d9-8945-6d343a7140b2" />

Next, From the WSL instance, copy the certificate file from windows to the ca-certificates folder and update the  "ca-certificates.conf" list.
```
sudo cp "/mnt/c/Users/xxxxxx/.../zscaler-ca.cer" /usr/share/ca-certificates/ZscalerRootCA.crt
echo "ZscalerRootCA.crt" | sudo tee -a /etc/ca-certificates.conf
sudo apt-get update
sudo update-ca-certificates --fresh
```
- Now, clone the playground repo
```
git clone https://github.com/nokia-eda/playground
cd playground
```
- Deploy EDA, it will fail due to certificates
```
export EXT_DOMAIN_NAME=localhost
make try-eda
```
- Stop when it fails and add the certificate to the kind node.
```
clab@C-5CG53743Q8:~$ docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS          PORTS                                                NAMES
bf67e50f83b7   kindest/node:v1.33.1   "/usr/local/bin/entr…"   56 minutes ago   Up 56 minutes   127.0.0.1:35789->6443/tcp, 0.0.0.0:9443->32767/tcp   eda-demo-control-plane
clab@C-5CG53743Q8:~$ echo "ZscalerRootCA.crt" | sudo tee -a /etc/ca-certificates.conf
ZscalerRootCA.crt
clab@C-5CG53743Q8:~$ docker cp zscaler-ca.cer bf67e50f83b7:/usr/local/share/ca-certificates/ZscalerRootCA.crt
Successfully copied 3.58kB to bf67e50f83b7:/usr/local/share/ca-certificates/ZscalerRootCA.crt
clab@C-5CG53743Q8:~$ docker exec -it bf67e50f83b7 update-ca-certificates
Updating certificates in /etc/ssl/certs...
rehash: warning: skipping ca-certificates.crt,it does not contain exactly one certificate or CRL
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.
clab@C-5CG53743Q8:~$
```
