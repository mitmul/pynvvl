#!/bin/bash

if [ $# -ne 1 ]; then
    echo 'Please specify CUDA version: e.g., "bash build.sh 9.0"'
    exit 1
fi

nvidia-docker run \
--rm \
-v $PWD:/root/build -t mitmul/pynvvl:cuda-$1 \
bash -c "find / -name \"*libnvcuvid.so.1\" | xargs -I{} ln -s {} /usr/local/lib/libnvcuvid.so && \
cd nvvl && mkdir build && cd build && \
cmake ../ && make -j && \
cp -r /usr/local/lib /root/build && \
cp libnvvl.so /root/build/lib && \
cp -r /root/nvvl/include /root/build/"
