import unittest
import app


class Acceptance(unittest.TestCase):
    def test_status_contract(self):
        self.assertEqual(app.status_label(429), "retry later")
        self.assertEqual(app.status_label(200), "ok")
        self.assertEqual(app.status_label(404), "missing")
        self.assertEqual(app.status_label(500), "unknown")


if __name__ == "__main__":
    unittest.main()
