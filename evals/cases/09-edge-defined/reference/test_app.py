import unittest
import app


class Tests(unittest.TestCase):
    def test_positive_limit(self):
        self.assertEqual(app.parse_limit("12"), 12)


    def test_empty_default(self):
        self.assertEqual(app.parse_limit(""), 20)


if __name__ == "__main__":
    unittest.main()
