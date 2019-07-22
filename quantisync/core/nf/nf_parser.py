import xmltodict
from xml.parsers.expat import ExpatError


class InvalidNf(Exception):
    def __init__(self, filePath):
        self.filePath = filePath

class InvalidXml(Exception):
    def __init__(self, filePath):
        self.filePath = filePath


def xmlToDict(xml):
    try:
        nf = xmltodict.parse(xml)
        return nf
    except ExpatError:
        raise InvalidXml


def removeUnusedTags(parsedNf):
    try:
        nfWithoutUnusedTags = parsedNf
        del nfWithoutUnusedTags['nfeProc']['NFe']['Signature']
        del nfWithoutUnusedTags['nfeProc']['protNFe']
        return nfWithoutUnusedTags
    except KeyError:
        raise InvalidNf


class NfParser:
    @classmethod
    def parse(cls, path):
        '''
        Converte um arquivo XML em um objeto Nf
        '''
        try:
            with open(path, 'r') as arquivo:
                xml = arquivo.read()
                nf = xmlToDict(xml)
                nfWithoutUnusedTags = removeUnusedTags(nf)
                return nfWithoutUnusedTags
        except IOError:
            raise
