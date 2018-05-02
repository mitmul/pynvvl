#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

from Cython.Distutils import build_ext
import numpy as np
from setuptools import Extension
from setuptools import setup
import subprocess

CUDA_VERSION = subprocess.check_output(
    'nvcc -V | grep -oP "release\s([0-9\.]+)" | grep -oP "([0-9\.]+)"',
    shell=True).decode('utf-8').strip()


def create_extensions():
    sourcefiles = [
        'pynvvl/nvvl.pyx',
    ]

    cpath = os.environ['CPATH'] if 'CPATH' in os.environ else ''
    includefiles = [
        'docker/include',
        '/usr/local/cuda/include',
        cpath,
        np.get_include()
    ]

    ld_library_path = os.environ['LD_LIBRARY_PATH'] \
        if 'LD_LIBRARY_PATH' in os.environ else ''
    library_dirs = [
        'docker/lib/cuda-{}'.format(CUDA_VERSION),
        ld_library_path
    ]

    libraries = [
        'nvvl',
    ]

    rpath = [
        '$ORIGIN/pynvvl/_lib',
    ]

    extensions = [
        Extension(
            'pynvvl',
            sourcefiles,
            include_dirs=includefiles,
            library_dirs=library_dirs,
            libraries=libraries,
            language='c++',
            extra_compile_args=['-std=c++11'],
            extra_link_args=['-std=c++11'],
            runtime_library_dirs=rpath,
        )
    ]
    return extensions


def prepare_package_data():
    wheel_libs = [
        'docker/lib/cuda-{}/libnvvl.so'.format(CUDA_VERSION),
        'docker/lib/cuda-{}/libavformat.so.57'.format(CUDA_VERSION),
        'docker/lib/cuda-{}/libavcodec.so.57'.format(CUDA_VERSION),
        'docker/lib/cuda-{}/libavutil.so.55'.format(CUDA_VERSION),
    ]
    lib_dir = 'pynvvl/_lib'
    if not os.path.exists(lib_dir):
        os.makedirs(lib_dir)
    libs = []
    for lib in wheel_libs:
        libname = os.path.basename(lib)
        libpath = os.path.join(lib_dir, libname)
        shutil.copy2(lib, libpath)
        libs.append(os.path.join('_lib', libname))

    package_data = {
        'pynvvl': libs
    }

    return package_data


package_data = prepare_package_data()
extensions = create_extensions()


setup(
    name='pynvvl',
    url='https://github.com/mitmul/pynvvl',
    version='0.0.1',
    author='Shunta Saito',
    author_email='shunta.saito@gmail.com',
    license='MIT',
    packages=['pynvvl'],
    package_data=package_data,
    # install_requires=['cupy>=4.0.0'],
    cmdclass={'build_ext': build_ext},
    ext_modules=extensions,
)
