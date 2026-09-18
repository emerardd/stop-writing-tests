import unittest
import app


class Acceptance(unittest.TestCase):
    def test_total_contract(self):
        self.assertEqual(app.total([(4, 2), (3, 1)]), 11)
        self.assertEqual(app.total([]), 0)


if __name__ == "__main__":
    unittest.main()
