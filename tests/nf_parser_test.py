import unittest
import collections

from quantisync.core.nf.nf_parser import NfParser, InvalidNf
from tests.config import FIXTURE_PATH


class NfParserTest(unittest.TestCase):

    def setUp(self):
        self.nf = NfParser.parse(FIXTURE_PATH / 'nfs1.XML')

    def test_output_dict(self):
        "Testa se produz dicionário"
        self.assertTrue(isinstance(self.nf, collections.Mapping))

    def test_output_valid_nf(self):
        "Testa se possui campo raiz da NF"
        self.assertTrue(self.nf['nfeProc']['NFe'])

    def test_output_nf_without_signature(self):
        "Testa se não possui campo Signature"
        with self.assertRaises(KeyError):
            self.nf['nfeProc']['NFe']['Signature']

    def test_output_nf_without_protocol(self):
        "Testa se não possui campo protNfe"
        with self.assertRaises(KeyError):
            self.nf['nfeProc']['protNFe']

    def test_output_invalid_nf_exception(self):
        "Testa se produz exception NfInvalida"
        with self.assertRaises(InvalidNf):
            NfParser.parse(FIXTURE_PATH / 'invalid1.XML')

        with self.assertRaises(InvalidNf):
            # Está falhando, falta tratar as outras versões da NF na removeUnusedTags
            NfParser.parse(FIXTURE_PATH / 'invalid2.XML')


if __name__ == '__main__':
    unittest.main()
