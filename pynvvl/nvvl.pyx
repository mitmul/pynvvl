from libcpp.string cimport string


cdef extern from "VideoLoader.h" namespace "NVVL":

    cdef cppclass VideoLoader:

        VideoLoader(int device_id) except +
        int frame_count(string filename)
        void read_sequence(string filename, int frame, int count=1)

        
cdef class NVVLVideoLoader:

    cdef VideoLoader* video_loader

    def __init__(self, device_id):
        self.video_loader = new VideoLoader(device_id)

    def frame_count(self, filename):
        return self.video_loader.frame_count(filename.encode('utf-8'))
