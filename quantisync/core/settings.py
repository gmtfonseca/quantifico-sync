import json
from pathlib import Path

from quantisync.config.storage import SETTINGS_PATH


class Settings:
    def __init__(self, nfsDir):
        self.nfsDir = nfsDir

    def toDict(self):
        return vars(self)

    @classmethod
    def fromJsonFile(cls, jsonFile):
        jsonDict = json.load(jsonFile)
        return cls(jsonDict['nfsDir'])

    @classmethod
    def empty(cls):
        return cls('')


class SettingsSerializer:
    def __init__(self, jsonPath=SETTINGS_PATH):
        self._jsonPath = Path(jsonPath)

    def load(self):
        if not self._jsonPath.exists():
            return Settings.empty()

        with self._jsonPath.open() as f:
            return Settings.fromJsonFile(f)

    def save(self, settings):
        if not self._jsonPath.parent.exists():
            self._jsonPath.parent.mkdir(parents=True, exist_ok=True)

        with self._jsonPath.open('w') as f:
            json.dump(settings.toDict(), f)
