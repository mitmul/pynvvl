#!/bin/bash

docker build -t mitmul/pynvvl:cuda-8.0 --build-arg CUDA_VERSION=8.0 -f Dockerfile.build-nvvl .
docker build -t mitmul/pynvvl:cuda-9.0 --build-arg CUDA_VERSION=9.0 -f Dockerfile.build-nvvl .
docker build -t mitmul/pynvvl:cuda-9.1 --build-arg CUDA_VERSION=9.1 -f Dockerfile.build-nvvl .

docker push mitmul/pynvvl:cuda-8.0
docker push mitmul/pynvvl:cuda-9.0
docker push mitmul/pynvvl:cuda-9.1
