#!/bin/bash

nvidia-docker run --rm -v $PWD:/root/build -ti mitmul/pynvvl \
bash -c "cd nvvl && mkdir build && cd build && \
cmake ../ && make -j && \
cp -r /usr/local/lib /root/build && \
cp libnvvl.so /root/build/lib && \
cp -r /root/nvvl/include /root/build/"
