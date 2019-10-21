import json
from pathlib import Path
from datetime import datetime

from quantisync.lib.util import Date


class UnableToSaveError(Exception):
    def __init__(self, message):
        self.message = message


class UnableToLoadError(Exception):
    def __init__(self, message):
        self.message = message


class SyncData:
    def __init__(self, nfsDir, userEmail, userOrg, lastSync):
        self.nfsDir = nfsDir
        self.userEmail = userEmail
        self.userOrg = userOrg
        self.lastSync = lastSync

    def toDict(self):
        return vars(self)

    @classmethod
    def fromJsonFile(cls, jsonFile):
        jsonDict = json.load(jsonFile)
        return cls(jsonDict['nfsDir'], jsonDict['userEmail'], jsonDict['userOrg'], jsonDict['lastSync'])

    @classmethod
    def empty(cls):
        return cls('', '', '', '')


class SyncDataModel:
    def __init__(self, jsonPath):
        self._jsonPath = Path(jsonPath)
        self._syncData = self.load()

    def setNfsDir(self, nfsDir):
        self._syncData.nfsDir = nfsDir
        self.save()

    def setUser(self, userEmail, userOrg):
        self._syncData.userEmail = userEmail
        self._syncData.userOrg = userOrg
        self.save()

    def setLastSync(self, lastSync):
        self._syncData.lastSync = lastSync
        self.save()

    def getSyncData(self):
        return self._syncData

    def load(self):
        try:
            if not self._jsonPath.exists():
                return SyncData.empty()

            with self._jsonPath.open() as f:
                syncData = SyncData.fromJsonFile(f)
                if syncData.lastSync:
                    syncData.lastSync = Date.parseString(syncData.lastSync)
                return syncData
        except Exception as err:
            raise UnableToLoadError(err)

    def save(self):
        try:
            if not self._jsonPath.parent.exists():
                self._jsonPath.parent.mkdir(parents=True, exist_ok=True)

            with self._jsonPath.open('w') as f:
                json.dump(self._syncData.toDict(), f, default=self._serializer)
        except Exception as err:
            raise UnableToSaveError(err)

    def remove(self):
        if self._jsonPath.exists():
            self._jsonPath.unlink()

    @property
    def jsonPath(self):
        return self._jsonPath

    def _serializer(self, o):
        if isinstance(o, datetime):
            return o.__str__()
