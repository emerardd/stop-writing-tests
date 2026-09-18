import unittest
import app


class Tests(unittest.TestCase):
    def test_request_timeout(self):
        self.assertEqual(app.request_timeout({}), 30)
        self.assertEqual(app.request_timeout({"timeout": 7}), 7)


if __name__ == "__main__":
    unittest.main()
