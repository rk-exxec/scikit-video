from numpy.testing import assert_equal
import numpy as np
import skvideo.io
import skvideo.utils
import skvideo.datasets
import os

# test read twice
def test_vread2x():
    for i in xrange(2):
        videodata = skvideo.io.vread(skvideo.datasets.bigbuckbunny())

def test_vread():
    videodata = skvideo.io.vread(skvideo.datasets.bigbuckbunny())

    T, M, N, C = videodata.shape

    # check the dimensions of the video

    assert_equal(T, 132)
    assert_equal(M, 720)
    assert_equal(N, 1280)
    assert_equal(C, 3)

    # check the numbers

    assert_equal(np.mean(videodata), 109.28332841215979)


# reading/writing consistency checks using real input data
def test_vread_raw():
    # reading first time
    bunnyMP4VideoData1 = skvideo.io.vread(skvideo.datasets.bigbuckbunny(), num_frames=1)
    skvideo.io.vwrite("bunnyMP4VideoData_vwrite.yuv", bunnyMP4VideoData1)

    # testing pipeline
    bunnyYUVVideoData1 = skvideo.io.vread("bunnyMP4VideoData_vwrite.yuv", width=1280, height=720, num_frames=1)
    skvideo.io.vwrite("bunnyYUVVideoData_vwrite.yuv", bunnyYUVVideoData1)
    bunnyYUVVideoData2 = skvideo.io.vread("bunnyYUVVideoData_vwrite.yuv", width=1280, height=720, num_frames=1)

    # reading second time, to test whether mutable defaults are set correctly
    bunnyMP4VideoData2 = skvideo.io.vread(skvideo.datasets.bigbuckbunny(), num_frames=1)

    # check the dimensions of the videos

    assert_equal(bunnyMP4VideoData1.shape, (1, 720, 1280, 3))
    assert_equal(bunnyMP4VideoData2.shape, (1, 720, 1280, 3))
    assert_equal(bunnyYUVVideoData1.shape, (1, 720, 1280, 3))
    assert_equal(bunnyYUVVideoData2.shape, (1, 720, 1280, 3))

    t = np.mean((bunnyMP4VideoData1 - bunnyMP4VideoData2)**2)
    assert t == 0, "Possible mutable default error in vread. MSE=%f between consecutive reads." % (t,)

    t = np.mean((bunnyMP4VideoData1 - bunnyYUVVideoData1)**2)
    assert t < 1, "Unacceptable precision loss (mse=%f) performing vwrite (mp4 data) -> vread (raw data)." % (t,)

    t = np.mean((bunnyYUVVideoData1 - bunnyYUVVideoData2)**2)
    assert t < 0.001, "Unacceptable precision loss (mse=%f) performing vwrite (raw data) -> vread (raw data)." % (t,)

    os.remove("bunnyMP4VideoData_vwrite.yuv")
    os.remove("bunnyYUVVideoData_vwrite.yuv")
