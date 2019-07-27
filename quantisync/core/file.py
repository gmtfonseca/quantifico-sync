class Properties:
    '''
    Estrutura de dados que descreve as propriedades e estado de um arquivo
    '''

    def __init__(self, name, modified):
        self.name = name
        self.modified = modified

    @classmethod
    def empty(cls):
        return cls('', 0)

    @classmethod
    def fromState(cls, state):
        '''
        Estado é uma string composta por '${nome}/${dataModificacaoSegundos}'
        '''
        if not state:
            return Properties.empty()

        nameModified = state.split('/')
        name = nameModified[0]
        modified = nameModified[1]
        return cls(name, modified)

    def getState(self):
        return '{}/{}'.format(self.name, self.modified)

    def toDict(self):
        return vars(self)
