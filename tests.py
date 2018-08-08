import unittest

from app import pdns_utils


class TestFunction(unittest.TestCase):
    def setUp(self):
        self.app = pdns_utils(config_name="testing")
        self.client = self.app.test_client
        self.zone = 'las1.marqeta.com'
        self.origin = '10.35.4'

    def test_fetch(self):
        # For whatever reason, flask test_client
        # doesnt support params in request call
        resp = self.client().get(f'/fetch/?zone={self.zone}&origin={self.origin}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('10.35.4', str(resp.data))


if __name__ == "__main__":
    unittest.main()
