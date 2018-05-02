pynvvl
======

## Requirements

- Docker
- nvidia-docker (v1/v2)
- CuPy v4.0.0

## Build

```
cd docker && bash build.sh [YOUR CUDA VERSION]
python setup.py build_ext -i
```

Please replace `[YOUR CUDA VERSION]` with 8.0/9.0/9.1 based on the CUDA version in your system.

## Usage

```
import pynvvl

loader = pynvvl.NVVLVideoLoader(device_id=0)

video = loader.read_sequence('examples/sample.mp4', 0, 2)

print(video.shape)  # => (2, 3, 256, 256)
print(video.dtype)  # => float32

import matplotlib.pyplot as plt

frame = video[0].get().transpose(1, 2, 0)
plt.imshow(frame)
plt.savefig('test.png')
```
