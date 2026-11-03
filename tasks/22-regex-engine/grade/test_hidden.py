import sys, os, unittest; sys.path.insert(0, os.getcwd())

import random, re, time
from rx import fullmatch
def gen(rnd, depth=0):
    r = rnd.random()
    if depth > 3 or r < 0.35:
        atom = rnd.choice(["a", "b", "c", ".", "[ab]", "[^a]", "[a-c]", "\\.", "d"])
    elif r < 0.55:
        atom = "(" + gen(rnd, depth + 1) + ")"
    elif r < 0.75:
        return gen(rnd, depth + 1) + gen(rnd, depth + 1)
    else:
        return "(" + gen(rnd, depth + 1) + "|" + gen(rnd, depth + 1) + ")"
    return atom + rnd.choice(["", "", "*", "+", "?"])
class T(unittest.TestCase):
    def test_basic(self):
        cases = [("", "", True), ("", "a", False), ("a", "a", True), ("a", "aa", False), ("a*", "", True),
                 ("(ab)+", "ababab", True), ("(ab)+", "aba", False), ("a|bc", "bc", True), ("[a-c]+d", "cabd", True),
                 ("[^a-c]", "d", True), ("[^a-c]", "b", False), ("\\.\\*", ".*", True), ("a\\|b", "a|b", True),
                 ("x.z", "xyz", True), ("(a|b)*c?", "abba", True), ("\\\\", "\\", True)]
        for p, t, want in cases:
            self.assertEqual(fullmatch(p, t), want, (p, t))
    def test_random_vs_re(self):
        rnd = random.Random(11)
        for _ in range(400):
            p = gen(rnd)
            for _ in range(6):
                t = "".join(rnd.choice("abcd.") for _ in range(rnd.randint(0, 7)))
                self.assertEqual(fullmatch(p, t), re.fullmatch(p, t) is not None, (p, t))
    def test_errors(self):
        for bad in ["(", "a)", "*a", "[ab", "a|*", "(?", "a\\", "a(*)"]:
            with self.assertRaises(ValueError, msg=bad):
                fullmatch(bad, "a")
    def test_pathological(self):
        t = time.perf_counter()
        self.assertTrue(fullmatch("a?" * 30 + "a" * 30, "a" * 30))
        self.assertFalse(fullmatch("(a*)*b", "a" * 40))
        self.assertLess(time.perf_counter() - t, 2)

if __name__ == "__main__":
    unittest.main()
