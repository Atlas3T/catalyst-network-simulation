echo "conda activate $(head -1 envs/environment.yml | cut -d' ' -f2)" >> ~/.bashrc
#make -C lib
#echo sudo locate jupyter-nbextension
#sudo locate jupyter-contrib
jupyter nbextensions_configurator enable --user
jupyter notebook --no-browser --ip=0.0.0.0

