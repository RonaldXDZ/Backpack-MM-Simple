import os
import shutil
import unittest
from unittest.mock import patch


class LighterSignerLoadingTestCase(unittest.TestCase):
    def setUp(self):
        from api.lighter_client import _CONTROLLED_SIGNER_DIR
        self.controlled_dir = _CONTROLLED_SIGNER_DIR
        self.filename = 'lighter-signer-darwin-arm64.dylib'
        self.fullpath = os.path.join(self.controlled_dir, self.filename)
        if not os.path.isfile(self.fullpath):
            self.skipTest('Signer library not present')

    @patch('platform.system', return_value='darwin')
    @patch('platform.machine', return_value='arm64')
    @patch('ctypes.CDLL', return_value=object())
    def test_load_from_controlled_dir_with_whitelist(self, *_):
        from api.lighter_client import SimpleSignerClient
        obj = SimpleSignerClient.__new__(SimpleSignerClient)
        lib = obj._load_library(None)
        self.assertIsNotNone(lib)

    @patch('platform.system', return_value='darwin')
    @patch('platform.machine', return_value='arm64')
    def test_reject_uncontrolled_dir(self, *_):
        from api.lighter_client import SimpleSignerClient, SimpleSignerError
        obj = SimpleSignerClient.__new__(SimpleSignerClient)
        with self.assertRaises(SimpleSignerError):
            obj._load_library('/tmp')

    @patch('platform.system', return_value='darwin')
    @patch('platform.machine', return_value='arm64')
    def test_hash_mismatch(self, *_):
        from api.lighter_client import SimpleSignerClient, SimpleSignerError
        tmpdir = os.path.join(self.controlled_dir, 'test_tmp')
        os.makedirs(tmpdir, exist_ok=True)
        target = os.path.join(tmpdir, self.filename)
        shutil.copyfile(self.fullpath, target)
        with open(target, 'ab') as f:
            f.write(b'0')
        obj = SimpleSignerClient.__new__(SimpleSignerClient)
        with self.assertRaises(SimpleSignerError):
            obj._load_library(tmpdir)


if __name__ == '__main__':
    unittest.main()

