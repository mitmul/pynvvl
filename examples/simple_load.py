#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pynvvl
import matplotlib.pyplot as plt

# Create NVVLVideoLoader object
loader = pynvvl.NVVLVideoLoader(device_id=0)

# Show the number of frames in the video
n_frames = loader.frame_count('examples/sample.mp4')
print('Number of frames:', n_frames)

# Load a video and return it as a CuPy array
video = loader.read_sequence(
    'examples/sample.mp4',
    horiz_flip=True,
    crop_y=30,
    crop_height=190,
    scale_method='Nearest',
    normalized=True
)

print(video.shape)  # => (91, 3, 256, 256): (n_frames, channels, height, width)
print(video.dtype)  # => float32

# Get the first frame as numpy array
frame = video[0].get()
frame = frame.transpose(1, 2, 0)

plt.imshow(frame)
plt.savefig('examples/sample.png')
