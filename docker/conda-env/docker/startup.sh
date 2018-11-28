echo "conda activate $(head -1 envs/environment.yml | cut -d' ' -f2)" >> ~/.bashrc
#make -C lib
jupyter nbextensions_configurator enable
jupyter notebook --no-browser --ip=0.0.0.0

