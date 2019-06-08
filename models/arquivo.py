import json


class Arquivo:

    def __init__(self, nome, dataUltimaModificacao, conteudo={}):
        self.nome = nome
        self.dataUltimaModificacao = dataUltimaModificacao
        self.conteudo = conteudo

    @classmethod
    def fromEstado(cls, estado):
        nomeDataUltimaModificacao = estado.split('/')
        nome = nomeDataUltimaModificacao[0]
        dataUltimaModificacao = nomeDataUltimaModificacao[1]
        return cls(nome, dataUltimaModificacao)

    def getEstado(self):
        return '{}/{}'.format(self.nome, self.dataUltimaModificacao)

    def toJSON(self):
        return json.dumps(vars(self))
