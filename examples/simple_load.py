#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pynvvl

loader = pynvvl.NVVLVideoLoader(device_id=0)

n_frames = loader.frame_count('examples/sample.mp4')

print(n_frames)

loader.read_sequence('examples/sample.mp4', 0, 1)
