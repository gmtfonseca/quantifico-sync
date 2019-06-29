
class NfHandler():
    def __init__(self, httpStreamQueue, httpDeleteQueue, NfInsercaoStrategy, NfRemocaoStrategy):
        self._httpStreamQueue = httpStreamQueue
        self._httpDeleteQueue = httpDeleteQueue
        self._NfInsercaoStrategy = NfInsercaoStrategy
        self._NfRemocaoStrategy = NfRemocaoStrategy

    def onInsercao(self, cliente, servidor, insercoes):
        nfInsercaoStrategy = self.NfInsercaoStrategy(cliente, servidor, self._httpStreamQueue)
        nfInsercaoStrategy.onInsercao(insercoes)

    def onRemocao(self, servidor, remocoes):
        nfRemocaoStrategy = self.NfRemocaoStrategy(servidor, self._httpDeleteQueue)
        nfRemocaoStrategy.onRemocao(remocoes)
