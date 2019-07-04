import logging


class Observador:
    """
    Detecta e propaga mudanças de estado entre Cliente e Servidor
    """

    def __init__(self, handler, cliente, servidor):
        self.handler = handler
        self.cliente = cliente
        self.servidor = servidor

    def observar(self):
        self.cliente.carregaEstado()

        remocoes = self._remocoes()
        insercoes = self._insercoes()

        if len(remocoes) > 0:
            logging.debug('remocao')
            print(remocoes)
            self.handler.onRemocao(self.servidor, remocoes)
        elif len(insercoes) > 0:
            logging.debug('insercao')
            print(insercoes)
            self.handler.onInsercao(self.cliente, self.servidor, insercoes)

    def _insercoes(self):
        return self.cliente.getEstado() - self.servidor.getEstado()

    def _remocoes(self):
        return self.servidor.getEstado() - self.cliente.getEstado()
