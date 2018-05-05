#!/bin/bash

if [ $# -ne 1 ]; then
    echo 'Please specify CUDA version: e.g., "bash build.sh 9.0"'
    exit 1
fi

nvidia-docker run \
--rm \
-v $PWD:/root/pynvvl -ti mitmul/pynvvl:cuda-$1-dev \
bash -c "find / -name \"*libnvcuvid.so.1\" | \
xargs -I{} ln -s {} /usr/local/lib/libnvcuvid.so && \
cd /root/nvvl && mkdir build && cd build && \
cd /root/nvvl/build && \
cmake ../ \
-DCMAKE_BUILD_WITH_INSTALL_RPATH=ON \
-DCMAKE_INSTALL_RPATH=\"\\\$ORIGIN\" && \
make -j && chrpath -l libnvvl.so && \
cd /root/pynvvl && \
bash
"
