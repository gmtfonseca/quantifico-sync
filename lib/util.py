import os
from pathlib import Path


class FileUtil:
    @staticmethod
    def baseName(path):
        if not path:
            return ""
        return Path(path).stem

    @staticmethod
    def lastModifDate(path):
        if not path:
            return ""
        return os.path.getmtime(path)
