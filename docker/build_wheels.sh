#!/bin/bash

nvidia-docker run --rm \
    -v $PWD:/pynvvl \
    -t mitmul/pynvvl:cuda-8.0 \
    rm -rf \
    /pynvvl/build \
    /pynvvl/dist \
    /pynvvl/docker/lib \
    /pynvvl/pynvvl_cuda80.egg-info \
    /pynvvl/pynvvl_cuda90.egg-info \
    /pynvvl/pynvvl_cuda91.egg-info \
    /pynvvl/pynvvl_cuda92.egg-info \
    /pynvvl/pynvvl_cuda100.egg-info \
    /pynvvl/pynvvl.egg-info 
bash docker/build_docker.sh
bash docker/build_nvvl.sh
python docker/build_wheels.py
