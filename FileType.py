class FileType:
    types = ['video', 'audio', 'text']

    def __init__(self, file_type: str) -> None:
        self.validate_type(f_type=file_type)
        self.file_type: str = file_type

    def validate_type(self, f_type: str) -> None:
        if f_type not in self.types:
            raise ValueError('Invalid file type')

    def __repr__(self):
        return self.file_type

    def __str__(self):
        return self.file_type
