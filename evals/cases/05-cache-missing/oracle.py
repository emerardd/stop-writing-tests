import unittest
import app


class Acceptance(unittest.TestCase):
    def test_expiration_contract(self):
        entry = {"value": "old", "expires_at": 10}
        self.assertEqual(app.cached_value(entry, 9), "old")
        self.assertIsNone(app.cached_value(entry, 10))
        self.assertIsNone(app.cached_value(entry, 11))


if __name__ == "__main__":
    unittest.main()
