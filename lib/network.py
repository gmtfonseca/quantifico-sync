import requests
from config.network import HTTP_CONFIG


class HttpService:

    def __init__(self, endpoint, url=HTTP_CONFIG['url']):
        self.url = url
        self.endpoint = endpoint

    def post(self, json):
        response = requests.post(self.url + self.endpoint, json=json).json()
        return response

    def put(self, json):
        response = requests.put(self.url + self.endpoint, json=json).json()
        return response

    def stream(self, data, streamGen):
        response = requests.post(
            self.url + self.endpoint, data=streamGen(data)).json()
        return response
