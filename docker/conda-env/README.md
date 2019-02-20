## Introduction

This docker container provides a ubuntu os with a python environment activated. It will start a Jupyter web application served to your localhost so that you can create and run python notebooks through your browser http://jupyter.org/.

Four local folders are mounted to the container's home directory. The files they contain can be accessed from within the container and any changes made from outside the container will be visible inside. NOTE any files saved inside the container will not persist when the container is stopped unless they are in one of these 4 folders. They are:

-simulation/python/sim (mounted to ~/lib)
all python modules in this folder are automatically added to the python environment. Any code you want to use in the container can be added to the existing python module simulation/python/sim/simlib).

-simulation/git-data (mounted to ~/git-data)
this folder should contain data that we want to feed into the simulation such as the JSON latency files. It is part of the git repo.

-simulation/notebooks (mounted to ~/notebooks)
jupyter notebooks for prototyping code and creating reports.

-[your local data folder] (mounted to ~/local-data)
for persisting results on your local machine while developing. This is not part of the git repo, as we don't want to store large data files there. When your code is deployed to the server the results will be recreated and stored in the server's own local-data folder.


## Setup

* Pull latest version of repository from master.

* Copy the .env file in simulation/docker/templates into simulation/docker/conda-env. Create a local folder outside the simulation repository where you want any results to be stored while you are working locally. Update the .env file so that the LOCAL_DATA_PATH variable points to your new folder.

* Sign in to atlas docker registry using
```shell
docker login -u adlnode adlnode.azurecr.io
```
* Pull the container image using 
```shell
docker pull adlnode.azurecr.io/conda
```
* In simulation/docker/conda-env type
```shell
docker-compose up
```
 to start the container. 

* On starting sucessfully it will print an address for you to paste into your browser to access the Jupyter web application. 

The container can be stopped by ctrl-c, and started again easily with `docker-compose up`.

## Notes

### Seeing which python packages are installed
In a Jupyter notebook you can use tab to autocomplete. This can help you to see what packages are already installed by typing
```python
import [tab]
```
or 
```python
from simlib import [tab]
```

### Adding python packages to the environment

If you want to add a new python package to the docker environment you can edit the file simulation/docker/conda-env/docker/environment.yml. You will then need to rebuild the container using
```shell
docker-compose up --build
```
You will also need to push this to the docker registry using
```shell
docker push adlnode.azurecr.io/conda
```

PS these two steps will take a loooong time. In the future I'll set the docker push to be triggered automatically when we push to master.
