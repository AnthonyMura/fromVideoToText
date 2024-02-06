from from_video_to_audio import vid_to_audio
from download_video import download_video_with_url

if __name__ == '__main__':
    vid_path = download_video_with_url()
    vid_to_audio(vid_path)
