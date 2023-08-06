import string


class Drive(int):
    pass


class ImagePath:
    def __init__(self, drive, path):
        self.drive = drive
        self._path = path

    @staticmethod
    def is_image_path(path):
        return len(path) > 1 and path[0] in string.digits and path[1] == ':'

    @staticmethod
    def split(drive_name, encoding):
        parts = drive_name.split(':', 1)
        return int(parts[0]), parts[1].encode(encoding)

    @classmethod
    def glob(cls, drive, name, image):
        return [cls(drive, p) for p in image.glob(name)]

    @classmethod
    def expand(cls, drive, name, image):
        return [cls(drive, p) for p in image.glob(name+b'*')]

    @property
    def file_type(self):
        return self._path.entry.file_type

    @property
    def size_bytes(self):
        return self._path.size_bytes

    @property
    def record_len(self):
        return self._path.entry.record_len

    def open(self, mode='r', ftype=None, record_len=None):
        return self._path.open(mode, ftype, record_len)

    def unlink(self):
        return self._path.unlink()

    def exists(self):
        return self._path.exists()

    def name(self, encoding):
        return self._path.name.decode(encoding)

    def __repr__(self):
        return "ImagePath({}:{})".format(self.drive, self._path.name)
