import unittest
import app


class Tests(unittest.TestCase):
    def test_unexpired(self):
        self.assertEqual(app.cached_value({"value": "fresh", "expires_at": 10}, 9), "fresh")


    def test_expiration_boundary(self):
        self.assertIsNone(app.cached_value({"value": "old", "expires_at": 10}, 10))


if __name__ == "__main__":
    unittest.main()
