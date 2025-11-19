# Testing EDA on WSL

## Installation 

- Get the base containerlab image from here https://github.com/srl-labs/wsl-containerlab/releases/tag/0.71.1-1.0 by downloading the .wsl file.
- Double clock on the .wsl file to install the distribution in wsl
- Connect to the image (wsl -d Containerlab)
- Clone the playground repo (+ skip some ca issues)
```
git config --global http.sslVerify false
git clone https://github.com/nokia-eda/playground
cd playground
```
