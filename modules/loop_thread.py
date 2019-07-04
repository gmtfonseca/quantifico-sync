from threading import Thread
import time


class LoopThread(Thread):

    def __init__(self, observador, notifyWindow, delay):
        super().__init__()
        self._observador = observador
        self._notifyWindow = notifyWindow
        self._delay = delay
        self._abort = False

    def run(self):
        while True:
            if self._abort:
                return

            self._observador.observar()
            time.sleep(self._delay)

    def abort(self):
        self._abort = True
