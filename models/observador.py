import time


class Observador:

    def __init__(self, handler, pastaCliente, pastaServidor, delay=60.0):
        self.handler = handler
        self.pastaCliente = pastaCliente
        self.pastaServidor = pastaServidor
        self.delay = delay

    def observar(self):
        while True:
            self.controlaMudancas()
            time.sleep(self.delay - time.time() % self.delay)

    def controlaMudancas(self):
        self.pastaCliente.atualizar()
        self.pastaServidor.atualizar()

        insercoes = self.insercoes()
        delecoes = self.delecoes()

        if len(delecoes) > 0:
            self.handler.onDelecao(delecoes)
        elif len(insercoes) > 0:
            self.handler.onInsercao(self.pastaCliente.getPath(), insercoes)

    def insercoes(self):
        return self.pastaCliente.getEstado() - self.pastaServidor.getEstado()

    def delecoes(self):
        return self.pastaServidor.getEstado() - self.pastaCliente.getEstado()
