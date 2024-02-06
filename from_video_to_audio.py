from pathlib import Path
from datetime import datetime

import os

# os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

from moviepy import editor as mp
from moviepy.config import change_settings


def vid_to_audio(vid_path: Path) -> None:
    clip_dir = Path.cwd() / 'clips'
    if not clip_dir.exists():
        clip_dir.mkdir()

    dir_date: str = datetime.now().strftime("%Y-%m-%d")
    file_date: str = datetime.now().strftime("%H-%M-%S")

    dir_date_path: Path = clip_dir / dir_date
    if not dir_date_path.exists():
        dir_date_path.mkdir()

    file_name = dir_date_path / f'{file_date}_{vid_path.name}.mp3'

    clip = mp.VideoFileClip(vid_path.as_posix())
    clip.audio.write_audiofile(file_name.as_posix())
