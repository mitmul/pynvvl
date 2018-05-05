#!/bin/bash

bash docker/build_docker.sh
sudo rm -rf docker/lib
bash docker/build_nvvl.sh
sudo rm -rf build dist *.egg-info
sudo rm -rf examples/*.txt examples/*.png
python docker/build_wheels.py
