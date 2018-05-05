ARG CUDA_VERSION=9.0
FROM mitmul/pynvvl:cuda-${CUDA_VERSION}

RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-pip \
    python3-tk \
    python3-dbg \
    ffmpeg \
    gdb \
    gawk \
    chrpath

RUN pip3 install \
    cython \
    numpy \
    matplotlib \
    imageio

ARG CUPY_PACKAGE_NAME
RUN pip3 install ${CUPY_PACKAGE_NAME}
