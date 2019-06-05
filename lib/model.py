import xmltodict


class Nf:

    def __init__(self, xml):
        self.xml = xml
        self.nf = {}

    def parse(self):
        nf = xmltodict.parse(self.xml)
        infeNfe = nf['nfeProc']['NFe']['infNFe']
        parsedNf = {
            'idSefaz': infeNfe['@Id'],
            'serie': infeNfe['ide']['serie'],
            'numero': infeNfe['ide']['nNF'],
            'dataEmissao': infeNfe['ide']['dhEmi'],
            'cliente': self.parseCliente(infeNfe['infNFe']['dest']),
            'saidas': self.parseSaidas(infeNfe['infNFe']['det']),
            'total': self.parseTotal(infeNfe['infNFe']['total'])
        }
        self.nf = parsedNf
        return self.nf

    def parseCliente(self, dest):
        return {
            'cnpj': dest['CNPJ'],
            'nome': dest['xNome'],
        }

    def parseSaidas(self, det):
        saidas = []
        for item in det:
            prod = item['prod']
            saidas.append({
                'produto': self.parseProduto(prod),
                'quantidade': prod['qCom'],
                'valorUnitario': prod['vUnCom'],
                'valorTotal': prod['vProd']
            })
        return saidas

    def parseProduto(self, produto):
        return {
            'codigo': produto['cProd'],
            'descricao': produto['xProd']
        }

    def parseTotal(self, total):
        return {
            'produtos': total['vProd'],
            'nf': total['vNF']
        }
