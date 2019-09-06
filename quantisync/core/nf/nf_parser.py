import xmltodict
from xml.parsers.expat import ExpatError


class InvalidNf(Exception):
    def __init__(self, filePath):
        self.filePath = filePath


def xmlToDict(xml):
    nf = xmltodict.parse(xml)
    return nf


def removeUnusedTags(parsedNf):
    nfWithoutUnusedTags = parsedNf
    try:
        del nfWithoutUnusedTags['nfeProc']['NFe']['Signature']
        del nfWithoutUnusedTags['nfeProc']['protNFe']
    except Exception:
        pass
    return nfWithoutUnusedTags


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
        except (ExpatError, KeyError):
            raise InvalidNf(path)
        except IOError:
            raise
