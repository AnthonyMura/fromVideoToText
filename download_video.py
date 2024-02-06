import re

from pathlib import Path
from pytube import YouTube
from datetime import datetime
from validators import url as url_validator


def check_if_dir_exists(dir_path: Path) -> None:
    """
    Check if directory exists. If not, create it.
    :param dir_path: Path object of directory to check or create it
    :return: None
    """
    if not dir_path.exists():
        dir_path.mkdir()


def check_if_video_exists(video_title: str) -> bool:
    """Check if video exists.
    :param video_title: Title of video contained only characters
    :return: True if video exists, False if not
    """
    video_dir = Path.cwd() / 'videos'
    videos = list(video_dir.rglob('*.mp4'))
    for existing_video_title in videos:
        if video_title in existing_video_title.name:
            return True


def download_video_with_url(url: None | str = None) -> None | Path:
    """
    Download video from URL.
    :param url: URL of video which should contains https://www.youtube.com
    :return: Path object of downloaded video
    """
    video_dir = Path.cwd() / 'videos'
    check_if_dir_exists(video_dir)

    if url is None:
        url = str(input("Enter URL: "))

    true_validation_condition = url_validator(url) and url.startswith('https://www.youtube.com')
    if true_validation_condition:
        yt = YouTube(url)

        download_date = datetime.now().strftime("%Y-%m-%d")
        download_dir = video_dir / download_date
        prefix_date = datetime.now().strftime("%H-%M-%S")

        check_if_dir_exists(download_dir)

        video = yt.streams.filter(progressive=True, file_extension='mp4') \
            .order_by('resolution') \
            .desc() \
            .first()

        title = yt.title
        title = re.sub('[!@#$|,._– -]', '', title)

        file_path: Path = download_dir / f'{prefix_date}_{title}.mp4'

        if not check_if_video_exists(title):
            print(f"Downloading {title}...")
            video.download(
                    filename_prefix=f'{prefix_date}_',
                    output_path=download_dir, filename=f'{title}.mp4'
                    )
            return file_path
        else:
            # TODO RENAME EXISTING FILE WITH NEW DATE OR CHANGE PREFIX FOR FURTHER MANIPULATION
            print(f"{title} already exists!")
            file_path.rename()
            return file_path
    else:
        raise ValueError("Invalid URL")
