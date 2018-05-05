import cupy

from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp cimport bool
from libc.stdint cimport uint16_t
from libc.stdint cimport uint8_t


cdef extern from "cuda_runtime.h":

    cdef struct CUstream_st
    ctypedef CUstream_st* cudaStream_t


cdef extern from "PictureSequence.h":

    ctypedef void* PictureSequenceHandle
    
    cdef PictureSequenceHandle nvvl_create_sequence(uint16_t count)

    cdef void nvvl_set_layer(
        PictureSequenceHandle sequence,
        const NVVL_PicLayer* layer,
        const char* name)

    cdef void nvvl_sequence_stream_wait(
        PictureSequenceHandle sequence,
        cudaStream_t stream)

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
    
    cdef PictureSequenceHandle nvvl_receive_frames_sync(
        VideoLoaderHandle loader, PictureSequenceHandle sequence);

    cdef struct Size:
        uint16_t width
        uint16_t height

    cdef Size nvvl_video_size(VideoLoaderHandle loader)


cdef class NVVLVideoLoader:

    cdef VideoLoaderHandle handle
    cdef int device_id

    def __init__(self, device_id):
        self.handle = nvvl_create_video_loader(device_id)
        self.device_id = device_id

    def __deaclloc__(self):
        nvvl_destroy_video_loader(self.handle)

    def frame_count(self, filename):
        return nvvl_frame_count(self.handle, filename.encode('utf-8'))

    def read_sequence(
            self, filename, frame=0, count=None, channels=3,
            scale_height=0, scale_width=0, crop_x=0, crop_y=0,
            crop_height=None, crop_width=None, scale_method='Linear',
            horiz_flip=False, normalized=False, color_space='RGB',
            chroma_up_method='Linear'):
        """Loads the video from disk and returns it as a CuPy ndarray.

        Args:
            filename (str): The path to the video.
            frame (int): The initial frame number of the returned sequence.
                Default is 0.
            count (int): The number of frames of the returned sequence.
                If it is None, whole frames of the video are loaded.
            channels (int): The number of color channels of the video.
                Default is 3.
            scale_height (int): The height of the scaled video.
                Note that scaling is performed before cropping.
                If it is 0 no scaling is performed. Default is 0.
            scale_width (int): The width of the scaled video.
                Note that scaling is performed before cropping.
                If it is 0, no scaling is performed. Default is 0.
            crop_x (int): Location of the crop within the scaled frame.
                Must be set such that crop_y + height <= original height.
                Default is 0.
            crop_y (int): Location of the crop within the scaled frame.
                Must be set such that crop_x + width <= original height.
                Default is 0.
            crop_height (int): The height of cropped region of the video.
                If it is None, no cropping is performed. Default is None.
            crop_width (int): The width of cropped region of the video.
                If it is None, no cropping is performed. Default is None.
            scale_method (str): Scaling method. It should be either of
                'Nearest' or 'Lienar'. Default is 'Linear'.
            horiz_flip (bool): Whether horizontal flipping is performed or not.
                Default is False.
            normalized (bool): If it is True, the values of returned video is
                normalized into [0, 1], otherwise the value range is [0, 255].
                Default is False.
            color_space (str): The color space of the values of returned video.
                It should be either 'RGB' or 'YCbCr'. Default is 'RGB'.
            chroma_up_method (str): How the chroma channels are upscaled from
                yuv 4:2:0 to 4:4:4. It should be 'Linear' currently.

        """
        frame_count = self.frame_count(filename)
        if count is None:
            count = frame_count
        if count > frame_count:
            raise ValueError(
                'count should be less than the video length ({}) '
                'but {} was given.'.format(frame_count, count))

        cdef PictureSequenceHandle sequence = nvvl_create_sequence(count)
        cdef Size size = nvvl_video_size(self.handle)
        cdef uint16_t width = size.width if crop_width is None else crop_width
        cdef uint16_t height = size.height if crop_height is None else crop_height
        cdef NVVL_PicLayer layer
        cdef string name = 'pixels'.encode('utf-8')

        with cupy.cuda.Stream() as stream:
            array = cupy.empty(
                (count, channels, height, width), dtype=cupy.float32)
            array = cupy.ascontiguousarray(array)
            stream.synchronize()

            layer.type = PDT_FLOAT
            layer.data = <void*><size_t>array.data.ptr
            layer.index_map = NULL
            layer.desc.count = count
            layer.desc.channels = channels
            layer.desc.height = height
            layer.desc.width = width
            layer.desc.crop_x = crop_x
            layer.desc.crop_y = crop_y
            layer.desc.scale_height = scale_height
            layer.desc.scale_width = scale_width
            layer.desc.horiz_flip = horiz_flip
            layer.desc.normalized = normalized

            if color_space == 'RGB':
                layer.desc.color_space = ColorSpace_RGB
            elif color_space == 'YCbCr':
                layer.desc.color_space = ColorSpace_YCbCr
            else:
                raise ValueError(
                    'color_space should be either \'RGB\' or \'YCbCr\' '
                    'but {} was given.'.format(color_space))

            if chroma_up_method == 'Linear':
                layer.desc.chroma_up_method = ChromaUpMethod_Linear
            else:
                raise ValueError(
                    'chroma_up_method should be \'Linear\' '
                    'but {} was given.'.format(chroma_up_method))

            if scale_method == 'Nearest':
                layer.desc.scale_method = ScaleMethod_Nearest
            elif scale_method == 'Linear':
                layer.desc.scale_method = ScaleMethod_Linear
            else:
                raise ValueError(
                    'scale_method should either \'Nearest\' or \'Linear\' '
                    'but {} was given.'.format(scale_method))

            layer.desc.stride.x = 1
            layer.desc.stride.y = width * layer.desc.stride.x
            layer.desc.stride.c = layer.desc.stride.y * height
            layer.desc.stride.n = layer.desc.stride.c * channels
            
            stream.record()
            nvvl_set_layer(sequence, &layer, name.c_str())
            nvvl_read_sequence(self.handle, filename.encode('utf-8'), frame, count)
            nvvl_receive_frames(self.handle, sequence)
            nvvl_sequence_stream_wait(
                sequence, <cudaStream_t><size_t>stream.ptr)
            nvvl_free_sequence(sequence)
            return array
