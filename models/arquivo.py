class Arquivo:

    def __init__(self, nome, dataModificacao, conteudo={}):
        self.nome = nome
        self.dataModificacao = dataModificacao
        self.conteudo = conteudo

    @classmethod
    def fromEstado(cls, estado):
        nomeDataModificacao = estado.split('/')
        nome = nomeDataModificacao[0]
        dataModificacao = nomeDataModificacao[1]
        return cls(nome, dataModificacao)

    def getEstado(self):
        return '{}/{}'.format(self.nome, self.dataModificacao)

    def toDict(self):
        return vars(self)
