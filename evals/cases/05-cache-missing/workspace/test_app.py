import unittest
import app


class Tests(unittest.TestCase):
    def test_unexpired(self):
        self.assertEqual(app.cached_value({"value": "fresh", "expires_at": 10}, 9), "fresh")


if __name__ == "__main__":
    unittest.main()
