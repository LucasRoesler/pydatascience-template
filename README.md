# pydatascience Template

A basic openfaas-template aimed at Python oriented data scientist.

The Docker image is based on Python3 and uses Conda for installing packages.

## Build options
1. `pillow`: will automatically add the build dependencies required to install Pillow

## Build Args
1.`ADDITIONAL_PACKAGE`: can be a list of additional packages that will be installed using apt-get
2. `CHANNEL`: specifies an additional conda channel that will be searched when installing python package

