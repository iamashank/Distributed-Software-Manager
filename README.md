# Distributed-Software-Manager

DSM is an installer that can install softwares downloaded from a distributed network. Each computer on a network acts as a Server that listens to software packages requests and replies if the software is available with it. Each client broadcast to check for the availability of package in the Local Network before downloading the packages from the Internet.

## Features:

* Can easily install multiple packages at once.
* Can remove and update packages.
* Can copy installed packages onto a external drive which can be used for setup on another Network.
* A distributed network ensures that a package is downloaded only once through the Internet throughout the Network.
* It also waits for other clients on the network to download the package (if they are already downloading it from the Internet) so that the client can download from the latter.

## Usage:

#### Installing packages
```
sudo python3 client.py install <package-name1> <package-name2> ....
```
#### Removing packages
```
sudo python3 client.py remove <package-name1> <package-name2> ....
```
#### Load packages from external drive
```
sudo python3 client.py load <drive-mount-address>
```
#### Load packages onto external drive
```
sudo python3 client.py store <drive-mount-address>
```
#### Start your own repository for distribution on Network
```
sudo python3 server.py
```
