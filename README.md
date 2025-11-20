# Testing EDA on WSL

## Installation 

Source mostly derived https://docs.eda.dev/25.4/software-install/non-production/wsl/ and related links + chatgpt :-)

Prerequisites: make sure wsl version is greater than 2.5
```
PS C:\Users\rirobert> wsl --version
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
- Clone the playground repo (+ skip some ca issues). I had some issue with ssl certs, so I skipped the check.
```
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo update-ca-certificates --fresh
git config --global http.sslVerify false
git clone https://github.com/nokia-eda/playground
cd playground
```
- 
