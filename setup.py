#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

import numpy as np

sourcefiles = [
    'pynvvl/nvvl.pyx',
]

cpath = os.environ['CPATH'] if 'CPATH' in os.environ else ''
includefiles = [
    'docker/include',
    '/usr/local/cuda/include',
    
    np.get_include()
]

ld_library_path = os.environ['LD_LIBRARY_PATH'] \
    if 'LD_LIBRARY_PATH' in os.environ else ''
library_dirs = [
    'docker/lib',
    ld_library_path
]

libraries = [
    'nvvl',
]

extensions = [
    Extension(
        "pynvvl",
        sourcefiles,
        include_dirs=includefiles, 
        library_dirs=library_dirs,
        libraries=libraries,
        language='c++',
        extra_compile_args=['-std=c++11'],
        extra_link_args=['-std=c++11'],
    )
]

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=extensions,
)
