import unittest
import app


class Acceptance(unittest.TestCase):
    def test_public_keys(self):
        self.assertEqual(app.request_timeout({}), 30)
        self.assertEqual(app.request_timeout({"timeout": 7}), 7)
        self.assertEqual(app.request_timeout({"timeout_seconds": 8}), 8)
        self.assertEqual(app.request_timeout({"timeout_seconds": 0, "timeout": 7}), 0)


if __name__ == "__main__":
    unittest.main()
