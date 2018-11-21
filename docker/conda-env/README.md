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


SETUP:

* Pull latest version of repository from master.

* Copy the .env file in simulation/docker/templates into simulation/docker/conda-env. Create a local folder outside the simulation repository where you want any results to be stored while you are working locally. Update the .env file so that the LOCAL_DATA_PATH variable points to your new folder.

*sign in to atlas docker registry using
'''sh
docker login -u cryptosregistry cryptosregistry.azurecr.io
'''

*in simulation/docker/conda-env type
'''sh
docker-compose up
'''
 to start the container. 

*If it starts sucessfully it will eventually print an address for you to paste into your browser to access the Jupyter web application. 



If you want to add a new python package to the docker environment you can edit the file simulation/docker/conda-env/docker/environment.yml. You will then need to rebuild the container using
'''sh
docker-compose up --build
'''
You will also need to push this to the docker registry using
'''sh
docker push cryptosregistry.azurecr.io/conda
'''
