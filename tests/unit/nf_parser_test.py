import unittest
import collections

from quantisync.core.nf.nf_parser import NfParser, XmlInvalido
from quantisync.core.nf.nf import NfInvalida
from tests.config import FIXTURE_PATH


class NfParserTest(unittest.TestCase):

    def setUp(self):
        self.nf = NfParser.parse(FIXTURE_PATH / 'local/nfs1.XML')

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
            NfParser.parse(FIXTURE_PATH / 'invalid/invalid1.XML')

    def test_nf_invalida_exception(self):
        "Testa se produz exception NfInvalida"
        with self.assertRaises(NfInvalida):
            NfParser.parse(FIXTURE_PATH / 'invalid/invalid2.XML')


if __name__ == '__main__':
    unittest.main()
