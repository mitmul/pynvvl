ARG cuda_version
FROM mitmul/pynvvl:cuda-${cuda_version}

ENV NVIDIA_DRIVER_CAPABILITIES=video,compute,utility

RUN apt-get update && apt-get install -y \
    python \
    python-dev \
    python-pip \
    python-wheel \
    python-setuptools \
    gawk \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    git

WORKDIR /root

ENV HOME /root

# Install pyenv.
RUN git clone https://github.com/pyenv/pyenv.git ${HOME}/.pyenv
ENV PYENV_ROOT ${HOME}/.pyenv
ENV PATH ${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PYENV_ROOT}/libexec:${PATH}
RUN eval "$(pyenv init -)"
RUN pyenv versions

# Install Python.
ARG python_versions
# RUN pyenv install 3.5.1
RUN for VERSION in ${python_versions}; do \
        echo "Installing Python ${VERSION}..." && \
        pyenv install ${VERSION} && \
        pyenv global ${VERSION} && \
        pyenv rehash && \
        echo "Finished"; \
    done;
RUN pyenv versions

# Install Python libraries.
ARG cython_version
ARG cupy_package_name
ARG cupy_version
RUN for VERSION in ${python_versions}; do \
        echo "Installing libraries on Python ${VERSION}..." && \
        pyenv global ${VERSION} && \
        pip install -U pip setuptools && \
        pip install argparse && \
        pip install Cython==${cython_version} wheel auditwheel && \
        pip install ${cupy_package_name}==${cupy_version} && \
        pip freeze; \
    done;

ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
