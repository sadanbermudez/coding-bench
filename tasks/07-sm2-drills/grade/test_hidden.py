import sys, os, unittest; sys.path.insert(0, os.getcwd())

from datetime import date
from drills.sm2 import Card, review, due
class T(unittest.TestCase):
    def test_sequence(self):
        c = review(Card(), 5); self.assertEqual((c.reps, c.interval), (1, 1)); self.assertAlmostEqual(c.ease, 2.6)
        c = review(c, 4); self.assertEqual((c.reps, c.interval), (2, 6)); self.assertAlmostEqual(c.ease, 2.6)
        c = review(c, 3); self.assertEqual(c.interval, round(6*2.6)); self.assertAlmostEqual(c.ease, 2.46)
    def test_fail(self):
        c = review(Card(reps=4, interval=30, ease=2.0), 2)
        self.assertEqual((c.reps, c.interval, c.ease), (0, 1, 2.0))
    def test_floor_immutable(self):
        start = Card(reps=3, interval=10, ease=1.31)
        c = review(start, 3)
        self.assertAlmostEqual(c.ease, 1.3); self.assertEqual(start.ease, 1.31)
    def test_bad(self):
        for q in (-1, 6, 2.5):
            with self.assertRaises(ValueError):
                review(Card(), q)
    def test_due(self):
        self.assertEqual(due(Card(interval=6), date(2026,12,28)), date(2027,1,3))

if __name__ == "__main__":
    unittest.main()
