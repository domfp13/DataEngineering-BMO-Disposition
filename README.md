# DataEngineering-APPUSMA206-BMO-Dispo
This is a replacement for the old legacy report BMO-Dispo that was installed in APPUSMA206. This code is being execute in a EC2 server and pulls out data from a Google SpreadSheet, after that extraction the data is cleaned up and finally is inserted into its corresponding bucket. 

## Getting Started
To test locally a decorator was added in GenericFuntions.py module, to test locally the decorator must be activated. 

### 1.- Installing the requirements
The code contains the requirements.txt, create a virtual env using this file before attempting to executed it. Once cloned, cd over the new directory.

```sh
$ git clone ~/DataEngineering-APPUSMA206-BMO-Dispo.git
$ conda create -n BMO-Dispo python=3.7
$ conda activate BMO-Dispo
$ pip install requirements.txt
```

## Authors
* **Luis Fuentes** - *2019-10-05*