import sys, os, unittest; sys.path.insert(0, os.getcwd())

import threading
from rag.chunk import chunk_words
def run(*a):
    box = {}
    th = threading.Thread(target=lambda: box.setdefault("r", chunk_words(*a)), daemon=True); th.start(); th.join(5)
    if th.is_alive(): raise AssertionError("hangs")
    return box["r"]
class T(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(run("a b c d e f g", 3, 1), ["a b c", "c d e", "e f g"])
        self.assertEqual(run("a b c d e f g h", 3, 1), ["a b c", "c d e", "e f g", "g h"])
        self.assertEqual(run("a  b\nc", 5, 2), ["a b c"])
        self.assertEqual(run("a b c d", 2, 0), ["a b", "c d"])
        self.assertEqual(run("", 3, 1), []); self.assertEqual(run("   ", 3, 1), [])
    def test_errors(self):
        for a in [(3, 3), (3, 4), (0, 0), (3, -1)]:
            with self.assertRaises(ValueError):
                chunk_words("a b c", *a)

if __name__ == "__main__":
    unittest.main()
