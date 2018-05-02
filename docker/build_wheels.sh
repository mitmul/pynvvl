#!/bin/bash

build_wheels () {
    nvidia-docker run \
    --rm \
    -v $PWD:/root/pynvvl -ti mitmul/pynvvl:cuda-$1-dev \
    bash -c "find / -name \"*libnvcuvid.so.1\" | \
    xargs -I{} ln -s {} /usr/local/lib/libnvcuvid.so && \
    cd /root/pynvvl && python3 setup.py bdist_wheel && \
    if [ ! -d dist/cuda-$1 ]; then mkdir -p dist/cuda-$1; fi && \
    ls dist/*.whl | xargs -I{} mv {} dist/cuda-$1/"
}

build_wheels 8.0
build_wheels 9.0
build_wheels 9.1
