from pathlib import Path


class File:

    def __init__(self, path):
        self._path = Path(path)

    def baseName(self):
        return self._path.stem

    def name(self):
        return self._path.name

    def modified(self):
        return self._path.stat().st_mtime

    def exists(self):
        return self._path.exists()

    def size(self):
        return self._path.stat().st_size

    def path(self):
        return str(self._path)


class Dir:

    def __init__(self, path):
        self._path = Path(path)

    def files(self, extension):
        return self._path.glob('*.{}'.format(extension))
