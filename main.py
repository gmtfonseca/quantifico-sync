import requests
import glob
from lib.util import FileUtil
from lib.model import Nf
import time
import pickle

PATH = 'nf/'
DELAY = 10.0


def request(nf):
    r = requests.post('http://localhost:3000/nfs', json=nf).json()
    print(r)
    # print(r.success)


def observe():
    serverState = loadServerState()
    while True:
        if (different(clientState(), serverState)):
            print('Diff')
        time.sleep(DELAY - time.time() % DELAY)


def different(clientState, serverState):
    return len(clientState - serverState) > 0 \
        or len(serverState - clientState) > 0


def loadServerState():
    with open("serverstate.file", "rb") as f:
        return pickle.load(f)


def sync(path):
    xml = open(path, 'r').read()
    nf = Nf(xml).parse()
    request(nf)


def clientState():
    xmls = glob.glob('{}*.XML'.format(PATH))
    return {
        '{}/{}'.
        format(FileUtil.baseName(f), FileUtil.lastModifDate(f)) for f in xmls
    }


def init():
    observe()
    # watchChanges()


init()
