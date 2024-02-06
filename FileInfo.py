import re

from pathlib import Path
from pytube import YouTube
from moviepy.editor import *
from datetime import datetime
from validators import url as url_validator

from FileType import FileType


def check_if_dir_exists(dir_path: Path) -> None:
    if not dir_path.exists():
        dir_path.mkdir()


def dir_path(file_type: FileType) -> Path:
    dir_p = Path.cwd() / str(file_type)
    check_if_dir_exists(dir_p)
    return dir_p


class FileInfo:
    YOUTUBE_URL = 'https://www.youtube.com'

    def __init__(self, url: str | None = None) -> None:
        self.url: str = self.validate_youtube_url(url=url)
        self.yt = YouTube(url=self.url)

        self.video = self.yt.streams \
            .filter(progressive=True, file_extension='mp4') \
            .order_by('resolution').desc().first()
        self.title: str = self.format_title()

        self.vid_dir_path: Path = dir_path(file_type=FileType("video"))
        self.audio_dir_path: Path = dir_path(file_type=FileType("audio"))

        self.download_date: str = datetime.now().strftime("%Y-%m-%d")
        self.download_index: str = datetime.now().strftime("H%HM%M")

        self.video_file_path: None | Path = None
        if not self.check_vid_existence():
            print(f"Downloading {self.title}...")
            self.video.download(
                    output_path=self.vid_dir_path,
                    filename=f"{self.download_date}_{self.download_index}_{self.title}.mp4"
                    )

    def format_title(self) -> str:
        title = re.sub('[!@#$|,._– -]', '', self.yt.title)
        return title

    def validate_youtube_url(self, url: str | None) -> str:
        if url is None:
            url = str(input("Enter URL: "))

        true_validation_condition = url_validator(url) and url.startswith(self.YOUTUBE_URL)
        if not true_validation_condition:
            raise ValueError("Invalid URL")
        return url

    def check_vid_existence(self) -> bool:
        videos = list(self.vid_dir_path.rglob('*.mp4'))
        videos_names = [v.name.split('_')[2] for v in videos]
        for v_index, v_name in enumerate(videos_names):
            if self.title in v_name:
                self.video_file_path = videos[v_index]
                print(f"Video already exists: {self.video_file_path}")
                return True

    def extract_audio_to_dir(self) -> None:
        print(f"Extracting {self.title} audio...")
        video = VideoFileClip(self.video_file_path.as_posix())
        audio_path = self.audio_dir_path / f"{self.video_file_path.stem}.mp3"
        print(audio_path.as_posix())
        video.audio.write_audiofile(audio_path.as_posix())
