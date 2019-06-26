import time


class Observador:

    def __init__(self, handler, cliente, servidor, delay=60.0):
        self.handler = handler
        self.cliente = cliente
        self.servidor = servidor
        self.delay = delay

    def observar(self):
        while True:
            self.detectaMudancas()
            time.sleep(self.delay - time.time() % self.delay)

    def detectaMudancas(self):
        self.cliente.atualizar()

        remocoes = self._remocoes()
        insercoes = self._insercoes()

        if len(remocoes) > 0:
            print('remocao')
            self.handler.onRemocao(self.servidor, remocoes)
        elif len(insercoes) > 0:
            print('insercao')
            self.handler.onInsercao(self.cliente, self.servidor, insercoes)

    def _insercoes(self):
        return self.cliente.getEstado() - self.servidor.getEstado()

    def _remocoes(self):
        return self.servidor.getEstado() - self.cliente.getEstado()
