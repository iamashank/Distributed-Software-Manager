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

[![DSM Demo Video](https://lh3.googleusercontent.com/uC2BfClWeiRMlddZUFBv2AIEbt1M2wnFJeAS9-QZmxfSBIS3neUz970ixJOZ_QA-mr3O-dwKn6zc0NwugczfRK-LpI4thHCX9zBMy5uPRiem0WB6m9AsSOq8AaANT5LWZTvyJolfCnMiGwP8lLUzDL9OZ0L42DgjTXWmWO5W6iGduaVEFc6EeMG4q7vUhaHCn2nLE-HuO3txIf8mUScCO5pTgrjpIze2tgv8iVA8wMNvEczeTfwcxIJ1PQn7to-Pnl2Z0fqqx8_gRaxOGEvCa6bRqt_y-R_ex8c-zgE2tTo41-UaL_uSCTqZeVrKUdyu7Y1ji92xmnpQjFJalh40Mxd0vxhEXAIdkrI2O3fsDTIUfLPDWIfqu8-5oWSv6_4V3-dIGsmLSov_HOm-so4qlaYp4Hsg1jgz4gX0FmBf0lQQ8rqzAIyqH1iroyr7HGhn1HMi7kArAzoEYELPDw7b9sM6kaXhl1MldOxOloz_l9qzNqVhjB-2hNwym0yDdc8DkPTGtNpCd7N9xzPakeBgQ7acV39Qwl6aqYwZSkPIYWsQbBDFefJFPoK3_y9NoE6IFxvZ1RE9NNQTVL844PsfHQbea1aBUDkfba9y-k8=w1006-h566-no)](https://drive.google.com/open?id=1UVTN_WRJ2xVtwz4X8NaJc69Ic184rOAI "DSM Demo Video")
