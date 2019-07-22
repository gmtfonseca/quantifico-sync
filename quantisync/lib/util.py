from pathlib import Path
import glob

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
    
    def unlink(self):
        return self._path.unlink()


class Dir:

    def __init__(self, path):
        self._path = Path(path)
    
    def files(self, extension):
        if self._path.exists():
            return glob.glob('{}/*.{}'.format(str(self._path), extension))                    
        else:
            return []
