import sys, os, unittest; sys.path.insert(0, os.getcwd())

import random, string, time
from dupes import near_duplicates
def slow(fps):
    return sorted((i, j) for i in range(len(fps)) for j in range(i+1, len(fps))
                  if sum(x != y for x, y in zip(fps[i], fps[j])) <= 1)
class T(unittest.TestCase):
    def test_small_matches_reference(self):
        rnd = random.Random(1)
        for L in (1, 2, 4):
            fps = ["".join(rnd.choice("abc") for _ in range(L)) for _ in range(60)]
            self.assertEqual(near_duplicates(fps), slow(fps), L)
    def test_big_fast(self):
        rnd = random.Random(7)
        fps = ["".join(rnd.choice(string.ascii_lowercase) for _ in range(12)) for _ in range(200_000)]
        fps[5] = fps[100]; fps[777] = fps[100][:3] + ("z" if fps[100][3] != "z" else "y") + fps[100][4:]
        t = time.perf_counter(); r = near_duplicates(fps); dt = time.perf_counter() - t
        self.assertLess(dt, 20, f"took {dt:.1f}s")
        for p in [(5, 100), (5, 777), (100, 777)]:
            self.assertIn(p, r)
        self.assertEqual(r, sorted(r))
        self.assertTrue(all(i < j for i, j in r))

if __name__ == "__main__":
    unittest.main()
