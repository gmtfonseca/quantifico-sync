from copy import deepcopy


class Nf:
    '''
    Estrutura de dados que representa uma Nota Fiscal
    '''

    def __init__(self, fileProperties, content):
        self.fileProperties = fileProperties
        self.content = content

    def toDict(self):
        selfCopy = deepcopy(self)
        selfCopy.fileProperties = selfCopy.fileProperties.toDict()
        return vars(selfCopy)
