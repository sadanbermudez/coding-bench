import sys, os, unittest; sys.path.insert(0, os.getcwd())

from chessrate.elo import expected_score, update
class T(unittest.TestCase):
    def test_expected(self):
        self.assertAlmostEqual(expected_score(2300, 2100), 0.7597, places=3)
        self.assertAlmostEqual(expected_score(2000, 2000), 0.5)
    def test_draw(self):
        self.assertLess(update(2300, 2100, 0.5), 2300)
        self.assertGreater(update(2100, 2300, 0.5), 2100)
        self.assertEqual(update(2300, 2100, 0.5), 2294.8)
    def test_win_k(self):
        self.assertEqual(update(2000, 2000, 1, k=10), 2005.0)
        self.assertEqual(update(2000, 2000, 0), 1990.0)

if __name__ == "__main__":
    unittest.main()
