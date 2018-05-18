#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pynvvl
import matplotlib.pyplot as plt
import cupy as cp


# Create NVVLVideoLoader object
loader = pynvvl.NVVLVideoLoader(device_id=0, log_level='error')

# Show the number of frames in the video
n_frames = loader.frame_count('examples/sample.mp4')
print('Number of frames:', n_frames)

# Prepare an output array
video = cp.empty((91, 3, 385, 512), dtype=cp.float32)

# Load a video and return it as a CuPy array
loader.read_sequence(
    'examples/sample.mp4',
    horiz_flip=True,
    scale_height=512,
    scale_width=512,
    crop_y=60,
    crop_height=385,
    crop_width=512,
    scale_method='Linear',
    normalized=True,
    out=video
)

print(video.shape)  # => (91, 3, 385, 512): (n_frames, channels, height, width)
print(video.dtype)  # => float32

# Get the first frame as numpy array
frame = video[0].get()
frame = frame.transpose(1, 2, 0)

plt.imshow(frame)
plt.savefig('examples/sample.png')
