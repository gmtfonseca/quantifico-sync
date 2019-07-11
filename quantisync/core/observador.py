class Observador:
    """
    Detecta mudanças de estado entre Cliente e Servidor
    """

    def __init__(self, cliente, servidor):
        self.cliente = cliente
        self.servidor = servidor
        self._insercoes = {}
        self._remocoes = {}

    def observar(self):
        self.cliente.carregaEstado()
        self._detectaInsercoes()
        self._detectaRemocoes()

    def _detectaInsercoes(self):
        self._insercoes = self.cliente.getEstado() - self.servidor.getEstado()

    def _detectaRemocoes(self):
        self._remocoes = self.servidor.getEstado() - self.cliente.getEstado()

    def possuiMudancas(self):
        return self.possuiInsercoes() or self.possuiRemocoes()

    def possuiInsercoes(self):
        return len(self._insercoes) > 0

    def possuiRemocoes(self):
        return len(self._remocoes) > 0

    def getInsercoes(self):
        return self._insercoes

    def getRemocoes(self):
        return self._remocoes
