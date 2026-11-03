import sys, os, unittest; sys.path.insert(0, os.getcwd())

import math
from moe import route, route_batch
class T(unittest.TestCase):
    def test_route(self):
        r = route([1.0, 3.0, 2.0, 3.0], 2)
        self.assertEqual([i for i, _ in r], [1, 3]); self.assertAlmostEqual(r[0][1], 0.5)
        r = route([0.0, 1000.0, 999.0], 2)
        self.assertAlmostEqual(r[0][1], 1 / (1 + math.exp(-1))); self.assertEqual(r[0][0], 1)
        self.assertAlmostEqual(sum(w for _, w in route([0.3, -2, 5, 1.1, 0], 3)), 1.0)
    def test_errors(self):
        for k in (0, 4):
            with self.assertRaises(ValueError):
                route([1, 2, 3], k)
    def test_capacity(self):
        b = [[5, 4, 0], [5, 0, 4], [5, 4, 0], [0, 0, 9]]
        r = route_batch(b, 2, capacity=2)
        self.assertEqual([i for i, _ in r[0]], [0, 1]); self.assertEqual([i for i, _ in r[1]], [0, 2])
        self.assertEqual(r[2], [(1, 1.0)])
        self.assertEqual([i for i, _ in r[3]], [2]); self.assertAlmostEqual(r[3][0][1], 1.0)
        r = route_batch([[1, 0], [1, 0]], 1, capacity=1)
        self.assertEqual(r[1], [])

if __name__ == "__main__":
    unittest.main()
