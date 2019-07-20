from quantisync.config.storage import LOG_PATH

# TODO - Implementar


class Logger:
    def __init__(self, path=LOG_PATH):
        self._path = path

    def append(self, text):
        self._path.write_text(text)
