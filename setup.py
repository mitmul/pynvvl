#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import subprocess
import sys
import sysconfig

from Cython.Distutils import build_ext
from pkg_resources import get_distribution
from setuptools import Extension
from setuptools import setup

CUDA_VERSION = subprocess.check_output(
    'nvcc -V | grep -oP "release\s([0-9\.]+)" | grep -oP "([0-9\.]+)"',
    shell=True).decode('utf-8').strip()


def create_extensions():
    sourcefiles = [
        'pynvvl/_nvvl.pyx',
    ]

    # List up include paths
    include_dirs = [
        os.path.join(os.getcwd(), 'docker/include'),
        '/usr/local/cuda/include',
        sysconfig.get_config_var('INCLUDEPY'),
    ]
    if 'CPATH' in os.environ:
        include_dirs.insert(1, os.environ['CPATH'])

    # List up library paths
    library_dirs = [
        os.path.join(os.getcwd(), 'docker/lib/cuda-{}'.format(CUDA_VERSION)),
    ]
    if 'LD_LIBRARY_PATH' in os.environ:
        library_dirs.append(os.environ['LD_LIBRARY_PATH'])
    if 'LIBRARY_PATH' in os.environ:
        library_dirs.append(os.environ['LIBRARY_PATH'])

    # List up libraries
    libraries = [
        'nvvl',
    ]

    # RPATH which will be set to pynvvl.so
    rpath = [
        '$ORIGIN/_lib',
    ]

    extensions = [
        Extension(
            'pynvvl._nvvl',
            sourcefiles,
            include_dirs=include_dirs,
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


parser = argparse.ArgumentParser()
parser.add_argument('--package-name', type=str, default='pynvvl')
args, sys.argv = parser.parse_known_args(sys.argv)

package_data = prepare_package_data()
extensions = create_extensions()

cupy_package_name = None
try:
    cupy_package_name = get_distribution(
        'cupy-cuda{}'.format(CUDA_VERSION.replace('.', '')))
    cupy_package_name = cupy_package_name.project_name
except Exception:
    cupy_package_name = 'cupy'

print('=' * 30)
print('CuPy Package Name:', cupy_package_name)
print('=' * 30)

description = \
    'PyNVVL: A Python wrapper for NVIDIA Video Loader (NVVL) with CuPy'

setup(
    name=args.package_name,
    url='https://github.com/mitmul/pynvvl',
    version='0.0.2a3',
    author='Shunta Saito',
    author_email='shunta.saito@gmail.com',
    description=description,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT License',
    packages=['pynvvl'],
    package_data=package_data,
    install_requires=[
        '{}>=4.0.0'.format(cupy_package_name),
    ],
    setup_requires=[
        'cython>=0.27.3',
    ],
    ext_modules=extensions,
    cmdclass={'build_ext': build_ext},
)
