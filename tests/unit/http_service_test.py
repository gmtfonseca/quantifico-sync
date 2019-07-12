import unittest
import mock

from requests.exceptions import HTTPError

from quantisync.lib.network import HttpService


class HttpServiceTest(unittest.TestCase):

    @mock.patch('quantisync.lib.network.requests.post')
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
