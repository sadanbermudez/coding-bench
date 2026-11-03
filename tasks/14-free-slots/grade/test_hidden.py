import sys, os, unittest; sys.path.insert(0, os.getcwd())

from datetime import datetime as DT
from calendar_tools import free_slots
def t(h, m=0): return DT(2026, 11, 2, h, m)
class T(unittest.TestCase):
    def test_merge(self):
        g = [(t(9), t(10)), (t(13), t(14))]
        o = [(t(9, 30), t(11)), (t(11), t(11, 30)), (t(16), t(15))]
        h = [(DT(2026, 11, 1, 22), t(8, 15)), (t(17, 30), DT(2026, 11, 3, 1))]
        self.assertEqual(free_slots([g, o, h], t(8), t(20), 30),
                         [(t(8, 15), t(9)), (t(11, 30), t(13)), (t(14), t(17, 30))])
    def test_exact_and_empty(self):
        self.assertEqual(free_slots([[(t(9), t(9, 30))]], t(9), t(10), 30), [(t(9, 30), t(10))])
        self.assertEqual(free_slots([], t(9), t(10), 61), [])
        self.assertEqual(free_slots([[]], t(9), t(10), 60), [(t(9), t(10))])

if __name__ == "__main__":
    unittest.main()
