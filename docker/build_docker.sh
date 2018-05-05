#!/bin/bash

build_docker_image() {
    docker build -t mitmul/pynvvl:cuda-$1 \
    --build-arg CUDA_VERSION=$1 \
    -f docker/Dockerfile.build-nvvl docker
    docker push mitmul/pynvvl:cuda-$1

    docker build -t mitmul/pynvvl:cuda-$1-dev \
    --build-arg CUDA_VERSION=$1 \
    --build-arg CUPY_PACKAGE_NAME=$2 \
    -f docker/Dockerfile.develop docker
    docker push mitmul/pynvvl:cuda-$1-dev
}

build_docker_image 8.0 cupy-cuda80
build_docker_image 9.0 cupy-cuda90
build_docker_image 9.1 cupy-cuda91
