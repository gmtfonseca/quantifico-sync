from config.network import HTTP_CONFIG
# TODO - Desacoplar estratégias de handler
from .nf_insercao_strategy import NfInsercaoStrategy
from .nf_remocao_strategy import NfRemocaoStrategy


class NfHandler():
    def __init__(self, httpService):
        self._httpService = httpService

    def onInsercao(self, cliente, servidor, insercoes):
        nfInsercaoStrategy = NfInsercaoStrategy(self._httpService,
                                                HTTP_CONFIG['batchSize']['insercao'],
                                                cliente,
                                                servidor)
        nfInsercaoStrategy.onInsercao(insercoes)

    def onRemocao(self, servidor, remocoes):
        nfRemocaoStrategy = NfRemocaoStrategy(self._httpService,
                                              HTTP_CONFIG['batchSize']['remocao'],
                                              servidor)
        nfRemocaoStrategy.onRemocao(remocoes)
