# TODO - Desacoplar estratégias de handler
from .nf_insercao_strategy import NfInsercaoStrategy
from .nf_remocao_strategy import NfRemocaoStrategy


class NfHandler():
    def __init__(self, httpService):
        self._httpService = httpService

    def onInsercao(self, cliente, servidor, insercoes):
        nfInsercaoStrategy = NfInsercaoStrategy(self._httpService,
                                                cliente,
                                                servidor)
        nfInsercaoStrategy.onInsercao(insercoes)

    def onRemocao(self, servidor, remocoes):
        nfRemocaoStrategy = NfRemocaoStrategy(self._httpService,
                                              servidor)
        nfRemocaoStrategy.onRemocao(remocoes)
