pynvvl
======

## Requirements

### For build

- nvidia-docker
- CuPy

### For use

- CuPy

## Build

```
cd docker && bash build.sh
python setup.py build_ext -i
```

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
