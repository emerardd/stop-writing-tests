import unittest
import app


class Tests(unittest.TestCase):
    def test_request_timeout(self):
        self.assertEqual(app.request_timeout({}), 30)
        self.assertEqual(app.request_timeout({"timeout": 7}), 7)


    def test_public_key_and_precedence(self):
        self.assertEqual(app.request_timeout({"timeout_seconds": 8}), 8)
        self.assertEqual(app.request_timeout({"timeout_seconds": 0, "timeout": 7}), 0)


if __name__ == "__main__":
    unittest.main()
