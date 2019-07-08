import os
from pathlib import Path


class ArquivoUtil:
    @staticmethod
    def nomeBase(path):
        if not path:
            return ""
        return Path(path).stem

    @staticmethod
    def dataModificacaoSegundos(path):
        if not path:
            return ""
        return os.path.getmtime(path)
