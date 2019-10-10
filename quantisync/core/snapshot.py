import pickle
from pathlib import Path
from http import HTTPStatus

from quantisync.core.file import Properties
from quantisync.lib.util import File, Dir


class LocalFolder(object):
    '''
    Representa uma pasta local com arquivos
    '''

    def __init__(self, path, extension, blacklistedFolder):
        self._path = path
        self._extension = extension
        self._blacklistedFolder = blacklistedFolder
        self._snapshot = set()

    def refresh(self):
        files = Dir(self._path).files(self._extension)
        self._snapshot = set()
        for f in files:
            try:
                self._snapshot.add(Properties(File(f).name(),
                                              File(f).modified())
                                   .getState())
            except FileNotFoundError:
                pass

    def clearBlacklistedFolder(self):
        if self._blacklistedFolder:
            self._blacklistedFolder.clear()

    def addToBlacklistFromPath(self, path, reason):
        fileProperties = Properties.fromPath(path)
        self._blacklistedFolder.addFile(fileProperties, reason)

    def addToBlacklistFromState(self, state, reason):
        fileProperties = Properties.fromState(state)
        self._blacklistedFolder.addFile(fileProperties, reason)

    def removeFromBlacklistIfExists(self, fileName):
        if self._blacklistedFolder.hasFile(fileName):
            self._blacklistedFolder.removeFile(fileName)

    def removeBlacklistedGhostFiles(self):
        blacklistedGhostFiles = self.getBlacklistedGhostFiles()
        for f in blacklistedGhostFiles:
            self._blacklistedFolder.removeFile(f)

    def getBlacklistedGhostFiles(self):
        blacklistedGhostFiles = []
        for f in self._blacklistedFolder.files:
            filePath = Path(self._path) / f
            invalidFile = File(filePath)
            if not invalidFile.exists():
                blacklistedGhostFiles.append(f)
        return blacklistedGhostFiles

    def hasBlacklistedGhostFiles(self):
        for f in self._blacklistedFolder.files:
            filePath = Path(self._path) / f
            invalidFile = File(filePath)
            if not invalidFile.exists():
                return True

    @property
    def blacklistedFolder(self):
        return self._blacklistedFolder

    @property
    def snapshot(self):
        return self._snapshot - self._blacklistedFolder.snapshot

    @property
    def path(self):
        return self._path

    @property
    def extension(self):
        return self._extension


class SerializableFolder(object):
    '''
    Representa um folder que pode ser gravado em disco
    '''

    def __init__(self, path):
        self._path = path

    def initialize(self, emptyObject):
        filePath = File(self._path)
        if not filePath.exists():
            self.saveToDisk(emptyObject)

        return self.loadFromDisk()

    def saveToDisk(self, obj):
        with open(self._path, "wb") as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def loadFromDisk(self):
        objectFile = File(self._path)
        if objectFile.size() > 0:
            with open(self._path, 'rb') as f:
                return pickle.load(f)

    def removeFromDisk(self):
        File(self._path).unlink()

    @property
    def path(self):
        return self._path


class CloudFolder(SerializableFolder):
    '''
    Set que representa o estado atual dos arquivos na nuvem
    '''

    def __init__(self, path, httpService):
        super().__init__(path)
        self._httpService = httpService
        self._snapshot = self.initialize(set())

    def setSnapshot(self, snapshot):
        self._snapshot = set(snapshot)
        self.saveToDisk(self._snapshot)

    def sync(self):
        response = self._httpService.get()
        print(response.json())
        if (response.status_code == HTTPStatus.OK):
            self.setSnapshot(response.json())
            print(self._snapshot)

    def getTotalFiles(self):
        return len(self._snapshot)

    def clear(self):
        self.setSnapshot(set())

    @property
    def snapshot(self):
        return self._snapshot


class BlacklistedFolder(SerializableFolder):
    '''
    Dicionário que representa arquivos considerados inválidos
    Sua chave é o nome completo do arquivo, já como valor possui seu estado
    '''

    def __init__(self, path):
        super().__init__(path)
        self._files = self.initialize(dict())

    def getReason(self, fileName):
        return self._files[fileName][1]

    def addFile(self, fileProperties, reason):
        if fileProperties and reason:
            self._files[fileProperties.name] = [fileProperties.getState(), reason]
            self.saveToDisk(self._files)

    def removeFile(self, fileName):
        self._files.pop(fileName)
        self.saveToDisk(self._files)

    def clear(self):
        self._files = dict()
        self.saveToDisk(self._files)

    def hasFile(self, fileName):
        return self._files and fileName in self._files

    def getTotalFiles(self):
        return len(self._files)

    @property
    def files(self):
        if not self._files:
            return set()

        return set(self._files.keys())

    @property
    def snapshot(self):
        if not self._files:
            return set()

        snapshot = set(f[0] for f in list(self._files.values()))
        return snapshot


class Observer(object):
    '''
    Responsável em detectar mudanças entre pasta local e pasta na nuvem
    '''

    def __init__(self, localFolder, cloudFolder):
        self._localFolder = localFolder
        self._cloudFolder = cloudFolder
        self._insertions = set()
        self._deletions = set()

    def observe(self):
        self._localFolder.refresh()
        self._updateInsertions()
        self._updateDeletions()

    def _updateInsertions(self):
        self._insertions = self._localFolder.snapshot - self._cloudFolder.snapshot

    def _updateDeletions(self):
        self._deletions = self._cloudFolder.snapshot - self._localFolder.snapshot

    def hasChanged(self):
        return self.hasInsertions() or self.hasDeletions() or self.hasBlacklistedGhostFiles()

    def hasInsertions(self):
        return len(self._insertions) > 0

    def hasDeletions(self):
        return len(self._deletions) > 0

    def hasBlacklistedGhostFiles(self):
        return self._localFolder.hasBlacklistedGhostFiles()

    @property
    def insertions(self):
        return self._insertions

    @property
    def deletions(self):
        return self._deletions

    @property
    def localFolder(self):
        return self._localFolder

    @property
    def cloudFolder(self):
        return self._cloudFolder
