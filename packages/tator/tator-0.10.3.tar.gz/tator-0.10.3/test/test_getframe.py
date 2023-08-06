import tator

from ._common import assert_vector_equal

def test_get_frame(host, token, project, video):
    tator_api = tator.get_api(host, token)
    video_obj = tator_api.get_media(video)

    frames = [50,100,150]
    file_path = tator_api.get_frame(video, frames=frames)
    frame_bgr = tator.util.get_images(file_path, video_obj)

    assert(len(frame_bgr) == 4)
    for frame_data in frame_bgr:
        size = (frame_data.height, frame_data.width, len(frame_data.mode))
        assert_vector_equal(size, (720,1280,3))
    

