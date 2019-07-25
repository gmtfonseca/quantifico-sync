import pickle

from quantisync.core.file import Properties
from quantisync.lib.util import File, Dir


class LocalFolder:
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
        self._snapshot = {Properties(File(f).name(),
                                     File(f).modified()).getState()
                          for f in files}

    def addInvalidFile(self, path):
        self._blacklistedFolder.add(path)

    def removeInvalidFile(self, fileName):
        self._blacklistedFolder.remove(fileName)

    def getSnapshot(self):
        return self._snapshot - self.getInvalidSnapshot()

    def getInvalidSnapshot(self):
        return self._blacklistedFolder.getSnapshot()

    def getPath(self):
        return self._path

    def getExtension(self):
        return self._extension


class SerializableFolder:
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

    def getPath(self):
        return self._path


class CloudFolder(SerializableFolder):
    '''
    Set que representa o estado atual dos arquivos na nuvem
    '''

    def __init__(self, path):
        super().__init__(path)
        self._snapshot = self.initialize(set())

    def setSnapshot(self, snapshot):
        self._snapshot = set(snapshot)
        self.saveToDisk(self._snapshot)

    def getSnapshot(self):
        return self._snapshot


class BlacklistedFolder(SerializableFolder):
    '''
    Dicionário que representa arquivos considerados inválidos
    Sua chave é o nome completo do arquivo, já como valor possui seu estado
    '''

    def __init__(self, path):
        super().__init__(path)
        self._files = self.initialize(dict())

    def add(self, path):
        invalidFile = File(path)
        if invalidFile.exists():
            fileName = invalidFile.name()
            fileProperties = Properties(invalidFile.name(), invalidFile.modified())
            self._files[fileName] = fileProperties.getState()
            self.saveToDisk(self._files)

    def remove(self, key):
        self._files.pop(key)
        self.saveToDisk(self._files)

    def getSnapshot(self):
        if self._files:
            return set(self._files.values())
        else:
            return set()


class Observer:
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
        self._insertions = self._localFolder.getSnapshot() - self._cloudFolder.getSnapshot()

    def _updateDeletions(self):
        self._deletions = self._cloudFolder.getSnapshot() - self._localFolder.getSnapshot()

    def hasChanged(self):
        return self.hasInsertions() or self.hasDeletions()

    def hasInsertions(self):
        return len(self._insertions) > 0

    def hasDeletions(self):
        return len(self._deletions) > 0

    def getInsertions(self):
        return self._insertions

    def getDeletions(self):
        return self._deletions

    def getLocalFolder(self):
        return self._localFolder

    def getCloudFolder(self):
        return self._cloudFolder
