import time


class Observador:

    def __init__(self, handler, cliente, servidor, delay=60.0):
        self.handler = handler
        self.cliente = cliente
        self.servidor = servidor
        self.delay = delay

    def observar(self):
        while True:
            self.controlaMudancas()
            time.sleep(self.delay - time.time() % self.delay)

    def controlaMudancas(self):
        self.cliente.atualizar()

        insercoes = self.insercoes()
        delecoes = self.delecoes()

        if len(delecoes) > 0:
            print('delecoes')
            self.handler.onDelecao(self.servidor, delecoes)
        elif len(insercoes) > 0:
            print('insercao')
            self.handler.onInsercao(self.cliente, self.servidor, insercoes)

    def insercoes(self):
        '''print('Estado cliente')
        print(self.cliente.getEstado())
        print('Estado servidor')
        print(self.servidor.getEstado())'''
        return self.cliente.getEstado() - self.servidor.getEstado()

    def delecoes(self):
        return self.servidor.getEstado() - self.cliente.getEstado()
