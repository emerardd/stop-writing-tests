import unittest
import app


class Acceptance(unittest.TestCase):
    def test_preserved_supported_input(self):
        self.assertEqual(app.parse_limit("12"), 12)


if __name__ == "__main__":
    unittest.main()
