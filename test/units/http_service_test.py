import unittest
from modules.lib.network import HttpService
from requests.exceptions import HTTPError
import mock


class HttpServiceTest(unittest.TestCase):

    @mock.patch('modules.lib.network.requests.post')
    def test_http_error_exception(self, mockRequestsPost):
        """
        Testa rota inválida
        """
        mockRequestsPost.side_effect = HTTPError
        httpService = HttpService('rota/valida')
        with self.assertRaises(HTTPError):
            httpService.post({
                'foo': 'bar'
            })


if __name__ == '__main__':
    unittest.main()
