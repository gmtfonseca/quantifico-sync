import unittest
from core.nf.nf_parser import NfParser, XmlInvalido
from core.nf.nf import NfInvalida
import collections


class NfParserTest(unittest.TestCase):

    def setUp(self):
        self.nf = NfParser.parse('tests/fixture/xml/2859.XML')

    def test_produz_dicionario(self):
        "Testa se produz dicionário"
        self.assertTrue(isinstance(self.nf, collections.Mapping))

    def test_produz_nf_valida(self):
        "Testa se possui campo raiz da NF"
        self.assertTrue(self.nf['nfeProc']['NFe'])

    def test_produz_nf_sem_assinatura(self):
        "Testa se não possui campo Signature"
        with self.assertRaises(KeyError):
            self.nf['nfeProc']['NFe']['Signature']

    def test_produz_nf_sem_protocolo(self):
        "Testa se não possui campo protNfe"
        with self.assertRaises(KeyError):
            self.nf['nfeProc']['protNFe']

    def test_xml_invalido_exception(self):
        "Testa se produz exception XmlInvalida"
        with self.assertRaises(XmlInvalido):
            NfParser.parse('tests/fixture/invalid/xml_invalido.XML')

    def test_nf_invalida_exception(self):
        "Testa se produz exception NfInvalida"
        with self.assertRaises(NfInvalida):
            NfParser.parse('tests/fixture/invalid/nf_invalida.XML')


if __name__ == '__main__':
    unittest.main()
