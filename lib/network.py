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

    def delete(self, json):
        response = requests.delete(self.url + self.endpoint, json=json).json()
        return response

    def stream(self, data, streamGenerator):
        response = requests.post(
            self.url + self.endpoint, data=streamGenerator(data)).json()
        return response
