import unittest
import app


class Acceptance(unittest.TestCase):
    def test_config_contract(self):
        self.assertEqual(app.request_timeout({}), 30)
        self.assertEqual(app.request_timeout({"timeout": 7}), 7)


if __name__ == "__main__":
    unittest.main()
