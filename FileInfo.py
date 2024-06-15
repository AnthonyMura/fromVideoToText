import re
import whisper
import logging

logging.getLogger().setLevel(logging.INFO)

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

        self.model = whisper.load_model("base")

        self.video = self.yt.streams \
            .filter(progressive=True, file_extension='mp4') \
            .order_by('resolution').desc().first()
        self.title: str = self.format_title()

        self.vid_dir_path: Path = dir_path(file_type=FileType("video"))
        self.audio_dir_path: Path = dir_path(file_type=FileType("audio"))
        self.text_dir_path: Path = dir_path(file_type=FileType("text"))

        self.download_date: str = datetime.now().strftime("%Y-%m-%d")
        self.download_index: str = datetime.now().strftime("H%HM%M")

        self.video_file_path: None | Path = None
        self.audio_file_path: None | Path = None
        self.text_file_path: None| Path = None

        self.text: None | str = None

        if not self.check_vid_existence():
            logging.info(f"Downloading {self.title}...")
            self.video.download(
                    output_path=self.vid_dir_path,
                    filename=f"{self.download_date}_{self.download_index}_{self.title}.mp4"
                    )
            self.video_file_path = self.vid_dir_path / f"{self.download_date}_{self.download_index}_{self.title}.mp4"
            logging.info(f"Downloaded successfully: {self.title}")
            self.extract_audio_to_dir()
            self.extract_text_from_audio()

        if self.audio_file_path is None:
            logging.info(f"Extracting {self.title} audio...")
            self.check_audio_existence()
        if self.text_file_path is None:
            logging.info(f"Extracting {self.title} text...")
            self.check_text_existence()


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
                logging.info(f"Video already exists: {self.video_file_path}")
                return True
        return False

    def check_audio_existence(self) -> None:
        audios = list(self.audio_dir_path.rglob('*.mp3'))
        audios_names = [a.name.split('_')[2] for a in audios]
        for a_index, a_name in enumerate(audios_names):
            if self.title in a_name:
                self.audio_file_path = audios[a_index]
                logging.info(f"Audio already exists: {self.audio_file_path}")
                return True
        return False

    def check_text_existence(self) -> None:
        texts = list(self.text_dir_path.rglob('*.txt'))
        texts_names = [t.name.split('_')[2] for t in texts]
        for t_index, t_name in enumerate(texts_names):
            if self.title in t_name:
                self.text_file_path = texts[t_index]
                logging.info(f"Text already exists: {self.text_file_path}")
                return True
        return False

    def extract_audio_to_dir(self) -> None:
        logging.info(f"Extracting {self.title} audio...")
        video = VideoFileClip(self.video_file_path.as_posix())
        audio_path = self.audio_dir_path / f"{self.video_file_path.stem}.mp3"
        logging.info(audio_path.as_posix())
        video.audio.write_audiofile(audio_path.as_posix())
        self.audio_file_path = audio_path

    def extract_text_from_audio(self) -> None:
        logging.info(f"Extracting {self.title} text...")
        audio = whisper.load_audio(self.audio_file_path.as_posix())
        text_result = self.model.transcribe(audio)
        self.text = text_result

        with open(self.text_dir_path / f"{self.video_file_path.stem}.txt", "w") as f:
            for segment in text_result["segments"]:
                f.write(f"{segment['text']}\n")


