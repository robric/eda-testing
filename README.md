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
- From the WSL instance, copy the certificate file from windows to the ca-certificates folder and update the  "ca-certificates.conf" list.
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
- Deploy EDA
```
export EXT_DOMAIN_NAME=localhost
make try-eda
```
