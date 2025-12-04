import unittest
from unittest.mock import patch
import requests


class LighterAccountIndexTestCase(unittest.TestCase):
    def test_timeout_and_error_handling(self):
        from api.lighter_client import _get_lihgter_account_index

        with patch('api.lighter_client.requests.get') as mock_get:
            mock_get.side_effect = requests.RequestException('network')
            with self.assertRaises(ValueError):
                _get_lihgter_account_index('0x0000000000000000000000000000000000000000')
            # 驗證帶有 timeout 參數
            try:
                mock_get.assert_called()
                _, kwargs = mock_get.call_args
                assert 'timeout' in kwargs and kwargs['timeout'] == 5
            except AssertionError:
                self.fail('requests.get 未使用超時參數')


if __name__ == '__main__':
    unittest.main()

