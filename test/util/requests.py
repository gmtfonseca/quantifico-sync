class MockResponse:
    def __init__(self, json, status_code):
        self._json = json
        self.status_code = status_code

    def json(self):
        return self._json
