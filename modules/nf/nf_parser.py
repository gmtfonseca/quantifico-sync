from xml.parsers.expat import ExpatError
import xmltodict


class XmlInvalido(Exception):
    # TODO - Trocar de module
    pass


class NfInvalida(Exception):
    pass


class NfParser:
    @classmethod
    def parse(cls, path):
        try:
            xml = open(path, 'r').read()
            parsedNf = xmltodict.parse(xml)
            del parsedNf['nfeProc']['NFe']['Signature']
            del parsedNf['nfeProc']['protNFe']
            return parsedNf
        except ExpatError:
            raise XmlInvalido
        except KeyError:
            raise NfInvalida
