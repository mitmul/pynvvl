PyNVVL
======

PyNVVL is a thin wrapper of NVIDIA Video Loader (NVVL). This packages enables you to load videos directoly to GPU memory and access them as CuPy ndarrays.

## Requirements

- CuPy v4.0.0

### For build

- Docker
- nvidia-docker (v1/v2)

## Build

```
cd docker && bash build_nvvl.sh [YOUR CUDA VERSION]
python setup.py build_ext -i
```

Please replace `[YOUR CUDA VERSION]` with 8.0/9.0/9.1 based on the CUDA version in your system.

## Usage

```python
import pynvvl

# Create NVVLVideoLoader object
loader = pynvvl.NVVLVideoLoader(device_id=0)

# Load a video and return it as a CuPy array
video = loader.read_sequence('examples/sample.mp4', frame=0, count=2)

print(video.shape)  # => (2, 3, 256, 256)
print(video.dtype)  # => float32

import matplotlib.pyplot as plt
frame = video[0].get().transpose(1, 2, 0)
plt.imshow(frame)
plt.show()
```

![](examples/sample.png)
