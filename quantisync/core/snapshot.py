import pickle

from quantisync.core.file import Properties
from quantisync.lib.util import File, Dir


class Client:

    """
    É uma pasta que contém um conjunto de propriedades de arquivos
    que determinam o estado do cliente
    """

    def __init__(self, path, extension, invalid):
        self._path = path
        self._extension = extension
        self._invalid = invalid

    def load(self):
        files = Dir(self._path).files(self._extension)
        self._snapshot = {Properties(File(f).baseName(),
                                     File(f).modified()).getState()
                          for f in files}
        self._snapshot = self._snapshot - self.getInvalidSnapshot()

    def addInvalidFile(self, path):
        self._invalid.add(path)

    def removeInvalidFile(self, fileName):
        self._invalid.remove(fileName)

    def getSnapshot(self):
        return self._snapshot

    def getInvalidSnapshot(self):
        self._invalid.load()
        return self._invalid.getSnapshot()

    def getPath(self):
        return self._path

    def getExtension(self):
        return self._extension


class Server:
    """
    É um pickle que caracteriza o estado do servidor
    """

    def __init__(self, path):
        self._path = path
        self.load()

    def load(self):
        snapshotFile = File(self._path)
        if not snapshotFile.exists():
            self._snapshot = set()
            self._saveToDisk()
        else:
            if snapshotFile.size() > 0:
                self._loadFromDisk()
            else:
                self._snapshot = set()

    def _saveToDisk(self):
        with open(self._path, "wb") as f:
            pickle.dump(self._snapshot, f, pickle.HIGHEST_PROTOCOL)

    def _loadFromDisk(self):
        with open(self._path, 'rb') as f:
            self._snapshot = pickle.load(f)

    def setSnapshot(self, snapshot):
        self._snapshot = set(snapshot)
        self._saveToDisk()

    def getSnapshot(self):
        return self._snapshot

    def getPath(self):
        return self._path


class Invalid:
    '''
    Dicionário que representa arquivos considerados inválidos
    '''

    def __init__(self, path):
        self._path = path

    def load(self):
        snapshotFile = File(self._path)
        if not snapshotFile.exists():
            self._snapshot = {}
            self._saveToDisk()
        else:
            if snapshotFile.size() > 0:
                self._loadFromDisk()
            else:
                self._snapshot = {}

    def add(self, path):
        invalidFile = File(path)
        if invalidFile.exists():
            key = invalidFile.name()
            fileProperties = Properties(invalidFile.baseName(), invalidFile.modified())
            self._snapshot[key] = fileProperties.getState()
            self._saveToDisk()

    def remove(self, key):
        self._snapshot.pop(key)
        self._saveToDisk()

    def _saveToDisk(self):
        with open(self._path, "wb") as f:
            pickle.dump(self._snapshot, f, pickle.HIGHEST_PROTOCOL)

    def _loadFromDisk(self):
        with open(self._path, 'rb') as f:
            self._snapshot = pickle.load(f)

    def getSnapshot(self):
        return set(self._snapshot.values())


class Observer:
    """
    Detecta mudanças de estado entre Cliente e Servidor
    """

    def __init__(self, client, server):
        self._client = client
        self._server = server
        self._insertions = {}
        self._deletions = {}

    def observe(self):
        self._client.load()
        self._observeInsertions()
        self._observeDeletions()

    def _observeInsertions(self):
        self._insertions = self._client.getSnapshot() - self._server.getSnapshot()

    def _observeDeletions(self):
        self._deletions = self._server.getSnapshot() - self._client.getSnapshot()

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
