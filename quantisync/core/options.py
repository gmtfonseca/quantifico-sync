import json
from pathlib import Path

from quantisync.config.storage import OPTIONS_PATH


class Options:
    def __init__(self, nfsPath):
        self.nfsPath = nfsPath

    def toDict(self):
        return vars(self)

    @classmethod
    def fromJsonFile(cls, jsonFile):
        jsonDict = json.load(jsonFile)
        return cls(jsonDict['nfsPath'])


class OptionsSerializer:
    def __init__(self, jsonPath=OPTIONS_PATH):
        self._jsonPath = Path(jsonPath)

    def load(self):
        if not self._jsonPath.exists():
            return Options('')

        with self._jsonPath.open() as f:
            return Options.fromJsonFile(f)

    def save(self, options):
        if not self._jsonPath.parent.exists():
            self._jsonPath.parent.mkdir(parents=True, exist_ok=True)

        with self._jsonPath.open('w') as f:
            json.dump(options.toDict(), f)
