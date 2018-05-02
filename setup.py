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

includefiles = [
    'docker/include',
    '/usr/local/cuda/include',
    os.environ['CPATH'],
    np.get_include()
]

library_dirs = [
    'docker/lib',
    os.environ['LD_LIBRARY_PATH']
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
