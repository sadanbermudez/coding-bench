import sys, os, unittest; sys.path.insert(0, os.getcwd())

from cache import TTLCache
class Clock:
    t = 0.0
    def __call__(self):
        return self.t
class T(unittest.TestCase):
    def setUp(self):
        self.c = Clock(); self.k = TTLCache(2, 10, clock=self.c)
    def test_lru(self):
        self.k.put("a", 1); self.k.put("b", 2); self.k.get("a"); self.k.put("c", 3)
        self.assertEqual(self.k.get("a"), 1); self.assertIsNone(self.k.get("b")); self.assertEqual(self.k.get("c"), 3)
    def test_ttl(self):
        self.k.put("a", 1); self.c.t = 9.9; self.assertEqual(self.k.get("a"), 1)
        self.c.t = 10; self.assertIsNone(self.k.get("a")); self.assertEqual(self.k.get("a", 7), 7)
    def test_expired_first(self):
        self.k.put("a", 1); self.c.t = 5; self.k.put("b", 2); self.c.t = 11
        self.k.get("b"); self.k.put("c", 3)
        self.assertEqual(self.k.get("b"), 2); self.assertEqual(self.k.get("c"), 3)
    def test_len_overwrite(self):
        self.k.put("a", 1); self.k.put("a", 2); self.assertEqual(len(self.k), 1); self.assertEqual(self.k.get("a"), 2)
        self.c.t = 20; self.assertEqual(len(self.k), 0)
    def test_bad(self):
        with self.assertRaises(ValueError):
            TTLCache(0, 1)

if __name__ == "__main__":
    unittest.main()
