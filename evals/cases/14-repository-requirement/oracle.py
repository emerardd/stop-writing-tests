import unittest
import app


class Acceptance(unittest.TestCase):
    def test_public_behavior(self):
        self.assertEqual(app.greeting("  ada  "), "Hello, Ada")
        self.assertEqual(app.greeting("lin"), "Hello, Lin")


if __name__ == "__main__":
    unittest.main()
