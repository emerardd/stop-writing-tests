import unittest
import app


class Tests(unittest.TestCase):
    def test_existing_statuses(self):
        self.assertEqual(app.status_label(200), "ok")
        self.assertEqual(app.status_label(404), "missing")
        self.assertEqual(app.status_label(500), "unknown")

    def test_rate_limit(self):
        self.assertEqual(app.status_label(429), "retry later")


if __name__ == "__main__":
    unittest.main()
