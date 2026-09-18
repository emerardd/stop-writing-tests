import unittest
import app


class Tests(unittest.TestCase):
    def test_access_contract(self):
        doc = {"owner_id": 1}
        self.assertTrue(app.can_read({"id": 1, "role": "member"}, doc))
        self.assertTrue(app.can_read({"id": 2, "role": "admin"}, doc))
        self.assertFalse(app.can_read({"id": 2, "role": "member"}, doc))


if __name__ == "__main__":
    unittest.main()
