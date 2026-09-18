import unittest
import app


class Acceptance(unittest.TestCase):
    def test_limit_contract(self):
        self.assertEqual(app.parse_limit("12"), 12)
        self.assertEqual(app.parse_limit(""), 20)


if __name__ == "__main__":
    unittest.main()
