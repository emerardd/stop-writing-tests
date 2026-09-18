import unittest
import app


class Tests(unittest.TestCase):
    def test_simple_greeting(self):
        self.assertEqual(app.greeting("Lin"), "Hello, Lin")


    def test_normalized_greeting(self):
        self.assertEqual(app.greeting("  ada  "), "Hello, Ada")


if __name__ == "__main__":
    unittest.main()
