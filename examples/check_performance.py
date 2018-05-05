#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import time

import imageio
import numpy as np

import cupy as cp
import pynvvl

video_fn = 'examples/sample.mp4'
N = 100

loader = pynvvl.NVVLVideoLoader(0)

time_pynvvl = []
for _ in range(N):
    st = time.time()
    video = loader.read_sequence(video_fn)
    time_pynvvl.append(time.time() - st)
print('PyNVVL: {} sec'.format(np.mean(time_pynvvl)))

cp.get_default_memory_pool().free_all_blocks()

time_imageio = []
for _ in range(N):
    st = time.time()
    video = imageio.mimread(video_fn)
    video = cp.asarray(video)
    time_imageio.append(time.time() - st)
print('ImageIO: {} sec'.format(np.mean(time_imageio)))
