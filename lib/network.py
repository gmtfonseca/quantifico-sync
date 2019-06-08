import requests
from config.network import HTTP_CONFIG


class HttpService:

    def __init__(self, endpoint, url=HTTP_CONFIG['url']):
        self.url = url
        self.endpoint = endpoint

    def post(self, json):
        response = requests.post(self.url + self.endpoint, json=json).json()
        return response
