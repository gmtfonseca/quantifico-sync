from xml.parsers.expat import ExpatError
from core.nf.nf import NfInvalida
import xmltodict


class XmlInvalido(Exception):
    # TODO - Trocar de module
    pass


def converteXmlParaDict(xml):
    try:
        nf = xmltodict.parse(xml)
        return nf
    except ExpatError:
        raise XmlInvalido


def removeTagsNaoUtilizadas(parsedNf):
    try:
        nfSemTagsNaoUtilizadas = parsedNf
        del nfSemTagsNaoUtilizadas['nfeProc']['NFe']['Signature']
        del nfSemTagsNaoUtilizadas['nfeProc']['protNFe']
        return nfSemTagsNaoUtilizadas
    except KeyError:
        raise NfInvalida


class NfParser:
    @classmethod
    def parse(cls, path):
        try:
            with open(path, 'r') as arquivo:
                xml = arquivo.read()
                nf = converteXmlParaDict(xml)
                nfSemAtributosNaoUtilizados = removeTagsNaoUtilizadas(nf)
                return nfSemAtributosNaoUtilizados
        except IOError:
            raise
