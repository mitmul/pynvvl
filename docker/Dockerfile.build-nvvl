ARG CUDA_VERSION=9.0
FROM nvidia/cuda:${CUDA_VERSION}-devel-ubuntu16.04

ARG FFMPEG_VERSION=3.4.2
ARG CMAKE_VERSION=3.10.2

# nvcuvid deps
RUN apt-get update --fix-missing && \
    apt-get install -y libx11-6 libxext6 vim git
ENV NVIDIA_DRIVER_CAPABILITIES=video,compute,utility

# minimal ffmpeg from source
RUN apt-get install -y yasm wget && \
    cd /tmp && wget -q http://ffmpeg.org/releases/ffmpeg-$FFMPEG_VERSION.tar.bz2 && \
    tar xf ffmpeg-$FFMPEG_VERSION.tar.bz2 && \
    rm ffmpeg-$FFMPEG_VERSION.tar.bz2 && \
    cd ffmpeg-$FFMPEG_VERSION && \
    ./configure \
      --prefix=/usr/local \
      --disable-static \
      --disable-all \
      --disable-autodetect \
      --disable-iconv \
      --enable-shared \
      --enable-avformat \
      --enable-avcodec \
      --enable-avfilter \
      --enable-protocol=file \
      --enable-demuxer=mov,matroska \
      --enable-bsf=h264_mp4toannexb,hevc_mp4toannexb && \
    make -j8 && make install && \
    cd /tmp && rm -rf ffmpeg-$FFMPEG_VERSION && \
    apt-get purge -y yasm wget && \
    apt-get autoremove -y

# video_reader build deps (pkg-config, Doxygen, recent cmake)
RUN apt-get install -y pkg-config doxygen wget && \
    cd /tmp && \
    export dir=$(echo $CMAKE_VERSION | sed "s/^\([0-9]*\.[0-9]*\).*/v\1/") && \
    wget -q https://cmake.org/files/${dir}/cmake-$CMAKE_VERSION-Linux-x86_64.sh && \
    /bin/sh cmake-$CMAKE_VERSION-Linux-x86_64.sh --skip-license --prefix=/usr/local && \
    rm cmake-$CMAKE_VERSION-Linux-x86_64.sh && \
    apt-get purge -y wget && \
    apt-get autoremove -y

ENV LD_LIBRARY_PATH /usr/local/lib:$LD_LIBRARY_PATH
ENV LIBRARY_PATH /usr/local/lib:$LIBRARY_PATH

WORKDIR /root

RUN git clone https://github.com/NVIDIA/nvvl.git
#     cd nvvl && mkdir build && cd build && \
#     cmake ../ && make -j && make install && \
#     cd .. && rm -rf nvvl
