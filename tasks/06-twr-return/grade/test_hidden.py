import sys, os, unittest; sys.path.insert(0, os.getcwd())

from datetime import date as D
from invest.returns import twr
class T(unittest.TestCase):
    def test_no_flows(self):
        self.assertAlmostEqual(twr([(D(2026,1,1),100),(D(2026,2,1),110),(D(2026,3,1),99)], []), -0.01)
    def test_flows(self):
        v = [(D(2026,1,1),1000),(D(2026,1,31),1100),(D(2026,2,28),1700)]
        f = [(D(2026,2,10),500),(D(2026,1,1),999)]
        # p1: 1100/1000-1 = .10 ; p2: (1700-500)/1100-1 = .090909
        self.assertAlmostEqual(twr(v, f), 1.1*(1200/1100)-1, places=9)
    def test_flow_on_end_date(self):
        v = [(D(2026,1,1),100),(D(2026,1,2),150)]
        self.assertAlmostEqual(twr(v, [(D(2026,1,2),50)]), 0.0)
    def test_withdrawal(self):
        v = [(D(2026,1,1),100),(D(2026,1,5),60)]
        self.assertAlmostEqual(twr(v, [(D(2026,1,3),-50)]), 0.10)
    def test_errors(self):
        with self.assertRaises(ValueError):
            twr([(D(2026,1,1),100)], [])
        with self.assertRaises(ValueError):
            twr([(D(2026,1,1),0),(D(2026,1,2),5)], [])

if __name__ == "__main__":
    unittest.main()
