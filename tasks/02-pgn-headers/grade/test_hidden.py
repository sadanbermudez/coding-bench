import sys, os, unittest; sys.path.insert(0, os.getcwd())

from pgn import parse_headers
PGN = (
    '[Event "Club \\"Open\\""]\n[White "Adan, Sergio"]\n[Black "X"]\n[Result "1-0"]\n\n'
    '1. e4 {a [comment] "quoted"} e5 2. Nf3 1-0\n\n'
    '[Event "Path"]\n[Site "C:\\\\games"]\n\n1. d4 d5 *\n'
)
class T(unittest.TestCase):
    def test_two(self):
        g = parse_headers(PGN)
        self.assertEqual(len(g), 2)
        self.assertEqual(g[0]["Event"], 'Club "Open"')
        self.assertEqual(g[0]["White"], "Adan, Sergio")
        self.assertEqual(g[0]["Result"], "1-0")
        self.assertEqual(len(g[0]), 4)
        self.assertEqual(g[1], {"Event": "Path", "Site": "C:\\games"})
    def test_empty(self):
        self.assertEqual(parse_headers(""), [])
        self.assertEqual(parse_headers("1. e4 e5 *\n"), [])

if __name__ == "__main__":
    unittest.main()
