import cupy

from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp cimport bool
from libc.stdint cimport uint16_t
from libc.stdint cimport uint8_t


cdef extern from "PictureSequence.h":

    ctypedef void* PictureSequenceHandle
    cdef PictureSequenceHandle nvvl_create_sequence(uint16_t count)
    cdef void nvvl_set_layer(
        PictureSequenceHandle sequence,
        const NVVL_PicLayer* layer,
        const char* name)
    cdef void nvvl_free_sequence(PictureSequenceHandle sequence)

    enum NVVL_ScaleMethod:
        ScaleMethod_Nearest
        ScaleMethod_Linear

    enum NVVL_ChromaUpMethod:
        ChromaUpMethod_Linear

    enum NVVL_ColorSpace:
        ColorSpace_RGB
        ColorSpace_YCbCr

    enum NVVL_PicDataType:
        PDT_NONE
        PDT_BYTE
        PDT_HALF
        PDT_FLOAT

    cdef struct stride:
        size_t x
        size_t y
        size_t c
        size_t n

    cdef struct NVVL_LayerDesc:

        uint16_t count
        uint8_t channels
        uint16_t width
        uint16_t height
        uint16_t crop_x
        uint16_t crop_y
        uint16_t scale_width
        uint16_t scale_height
        bool horiz_flip
        bool normalized
        NVVL_ColorSpace color_space
        NVVL_ChromaUpMethod chroma_up_method
        NVVL_ScaleMethod scale_method
        stride stride

    cdef struct NVVL_PicLayer:

        NVVL_PicDataType type
        NVVL_LayerDesc desc
        const int* index_map
        int index_map_length
        void* data


cdef extern from "VideoLoader.h":

    ctypedef void* VideoLoaderHandle
    cdef VideoLoaderHandle nvvl_create_video_loader(int device_id)
    cdef void nvvl_destroy_video_loader(VideoLoaderHandle loader)
    cdef int nvvl_frame_count(VideoLoaderHandle loader, const char* filename)
    cdef void nvvl_read_sequence(
        VideoLoaderHandle loader, const char* filename, int frame, int count)
    cdef PictureSequenceHandle nvvl_receive_frames(
        VideoLoaderHandle loader, PictureSequenceHandle sequence);

    cdef struct Size:
        uint16_t width
        uint16_t height

    cdef Size nvvl_video_size(VideoLoaderHandle loader)


# cdef extern from "cuda_runtime.h":
#
#     cdef void cudaMallocPitch(void** devPtr, size_t* pitch, size_t width, size_t height)


cdef class NVVLVideoLoader:

    cdef VideoLoaderHandle handle

    def __init__(self, device_id):
        self.handle = nvvl_create_video_loader(device_id)

    def __deaclloc__(self):
        nvvl_destroy_video_loader(self.handle)

    def frame_count(self, filename):
        return nvvl_frame_count(self.handle, filename.encode('utf-8'))

    def read_sequence(
            self, filename, frame=0, count=None, channels=3, crop_height=None,
            crop_width=None, scale_height=1.0, scale_width=1.0,
            horiz_flip=False, normalized=True, color_space='RGB'):
        if count is None:
            count = self.frame_count(filename)
        cdef PictureSequenceHandle sequence = nvvl_create_sequence(count)

        cdef Size size = nvvl_video_size(self.handle)
        cdef uint16_t width = size.width if crop_width is None else crop_width
        cdef uint16_t height = size.height if crop_height is None else crop_height

        cdef size_t pitch = 0
        array = cupy.zeros((count, channels, height, width), dtype=cupy.float32)
        
        cdef NVVL_PicLayer layer
        layer.type = PDT_FLOAT
        layer.data = <float*><size_t>array.data.ptr
        layer.desc.count = count
        layer.desc.channels = channels
        layer.desc.height = height
        layer.desc.width = width
        layer.desc.scale_height = scale_height
        layer.desc.scale_width = scale_width
        layer.desc.horiz_flip = horiz_flip
        layer.desc.normalized = normalized

        cdef NVVL_ColorSpace nvvl_color_space
        if color_space == 'RGB':
            nvvl_color_space = ColorSpace_RGB
        elif color_space == 'YCbCr':
            nvvl_color_space = ColorSpace_YCbCr
        layer.desc.color_space = nvvl_color_space

        layer.desc.stride.x = 1
        layer.desc.stride.y = pitch / sizeof(float)
        layer.desc.stride.c = layer.desc.stride.y * height
        layer.desc.stride.n = layer.desc.stride.c * channels

        #cudaMallocPitch(
        #    &layer.data, &layer.desc.stride.y, layer.desc.width,
        #    layer.desc.height * count * channels)
        
        nvvl_set_layer(sequence, &layer, 'pixels')

        nvvl_read_sequence(self.handle, filename.encode('utf-8'), frame, count)
        nvvl_receive_frames(self.handle, sequence)
        #nvvl_free_sequence(sequence)
