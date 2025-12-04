import os
import importlib
import unittest


class WebAuthTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['ADMIN_TOKEN'] = 'testtoken'
        # 重新載入服務器模塊以應用新的環境變量
        self.server = importlib.import_module('web.server')
        importlib.reload(self.server)
        self.app = self.server.app.test_client()

    def test_start_without_token(self):
        resp = self.app.post('/api/start', json={'exchange': 'backpack', 'symbol': 'SOL_USDC', 'spread': 0.1})
        self.assertEqual(resp.status_code, 401)

    def test_start_with_wrong_token(self):
        resp = self.app.post('/api/start',
                             headers={'Authorization': 'Bearer wrong'},
                             json={'exchange': 'backpack', 'symbol': 'SOL_USDC', 'spread': 0.1})
        self.assertEqual(resp.status_code, 401)

    def test_start_with_correct_token(self):
        resp = self.app.post('/api/start',
                             headers={'Authorization': 'Bearer testtoken'},
                             json={'exchange': 'backpack', 'symbol': 'SOL_USDC', 'spread': 0.1})
        # 未配置 API 憑證時應返回 400（而不是 401）
        self.assertEqual(resp.status_code, 400)


if __name__ == '__main__':
    unittest.main()

