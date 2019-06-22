import requests
from config.network import HTTP_CONFIG
import xmltodict
import json
import time

url = HTTP_CONFIG['url']

file1 = open('./nf/2859.XML', 'rb').read()
file2 = open('./nf/2860.XML', 'rb').read()
file3 = open('./nf/2862.XML', 'rb').read()
file4 = open('./nf/2863.XML', 'rb').read()
file5 = open('./nf/2864.XML', 'rb').read()
file6 = open('./nf/2865.XML', 'rb').read()
file7 = open('./nf/2866.XML', 'rb').read()
file8 = open('./nf/2867.XML', 'rb').read()
file9 = open('./nf/2889.XML', 'rb').read()
file10 = open('./nf/2928.XML', 'rb').read()

arquivos = []

arquivos.append({
    'nome': '2859',
    'dataModificacao': '0000',
    'conteudo': xmltodict.parse(file1)
})

arquivos.append({
    'nome': '2860',
    'dataModificacao': '6666',
    'conteudo': xmltodict.parse(file2)
})

arquivos.append({
    'nome': '2862',
    'dataModificacao': '9999',
    'conteudo': xmltodict.parse(file3)
})

arquivos.append({
    'nome': '2863',
    'dataModificacao': '9999',
    'conteudo': xmltodict.parse(file4)
})

arquivos.append({
    'nome': '2864',
    'dataModificacao': '9999',
    'conteudo': xmltodict.parse(file5)
})

arquivos.append({
    'nome': '2865',
    'dataModificacao': '9999',
    'conteudo': xmltodict.parse(file6)
})

arquivos.append({
    'nome': '2866',
    'dataModificacao': '9999',
    'conteudo': xmltodict.parse(file7)
})

arquivos.append({
    'nome': '2867',
    'dataModificacao': '9999',
    'conteudo': xmltodict.parse(file8)
})

arquivos.append({
    'nome': '2889',
    'dataModificacao': '9999',
    'conteudo': xmltodict.parse(file9)
})

arquivos.append({
    'nome': '2928',
    'dataModificacao': '9999',
    'conteudo': xmltodict.parse(file10)
})


def gen():
    for arquivo in arquivos:
        yield json.dumps(arquivo, ensure_ascii=False).encode()
        # time.sleep(0.01)

    # yield json.dumps(a, ensure_ascii=False)


response = requests.get(url + 'nfs').json()
print(response)
