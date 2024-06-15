from FileInfo import FileInfo


if __name__ == '__main__':
    file = FileInfo()
    if file.video_file_path.exists():
        file.extract_audio_to_dir()
    if file.audio_file_path.exists():
        file.convert_to_text()