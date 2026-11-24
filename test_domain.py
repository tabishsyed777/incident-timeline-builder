import unittest
import core

class DomainTests(unittest.TestCase):
    def test_offsets(self):
        rows=core.read(core.DEFAULT)
        rows[1]["time"]="2025-05-01T14:30:00+05:30"
        self.assertIn("09:00:00Z",core.answer(rows,"first event for atlas")["answer"])

    def test_naive_time(self):
        rows=core.read(core.DEFAULT)
        rows[0]["time"]="2025-01-01T01:00:00"
        with self.assertRaises(ValueError): core.validate(rows)

    def test_challenge_queries(self):
        rows=core.validate(core.read(core.DEFAULT))
        for query,expected in core.read(core.DEFAULT.parent.parent/"qa/challenge.json"):
            with self.subTest(query=query):
                self.assertEqual(core.answer(rows,query)["answer"],expected)
