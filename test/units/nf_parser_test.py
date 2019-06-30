import unittest
from modules.nf.nf_parser import NfParser, XmlInvalido
from modules.nf.nf import NfInvalida
import collections


class NfParserTest(unittest.TestCase):

    def setUp(self):
        self.nf = NfParser.parse('test/fixture/xml/2859.XML')

    def testa_produz_dicionario(self):
        "Testa se produz dicionário"
        self.assertTrue(isinstance(self.nf, collections.Mapping))

    def testa_produz_nf_valida(self):
        "Testa se possui campo raiz da NF"
        self.assertTrue(self.nf['nfeProc']['NFe'])

    def testa_produz_nf_sem_assinatura(self):
        "Testa se não possui campo Signature"
        with self.assertRaises(KeyError):
            self.nf['nfeProc']['NFe']['Signature']

    def testa_produz_nf_sem_protocolo(self):
        "Testa se não possui campo protNfe"
        with self.assertRaises(KeyError):
            self.nf['nfeProc']['protNFe']

    def testa_xml_invalido_exception(self):
        "Testa se produz exception XmlInvalida"
        with self.assertRaises(XmlInvalido):
            NfParser.parse('test/fixture/invalid/xml_invalido.XML')

    def testa_nf_invalida_exception(self):
        "Testa se produz exception NfInvalida"
        with self.assertRaises(NfInvalida):
            NfParser.parse('test/fixture/invalid/nf_invalida.XML')


if __name__ == '__main__':
    unittest.main()
