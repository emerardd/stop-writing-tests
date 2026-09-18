import unittest
import app


class Tests(unittest.TestCase):
    def test_greeting(self):
        self.assertEqual(app.greeting("  ada  "), "Hello, Ada")


if __name__ == "__main__":
    unittest.main()
