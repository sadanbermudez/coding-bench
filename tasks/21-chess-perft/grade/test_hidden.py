import sys, os, unittest; sys.path.insert(0, os.getcwd())

import time
from perft import perft, legal_moves
START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
KIWI = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
P3 = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1"
P4 = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
P5 = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"
class T(unittest.TestCase):
    def test_moves(self):
        m = legal_moves(START)
        self.assertEqual(len(m), 20); self.assertIn("e2e4", m); self.assertIn("g1f3", m); self.assertEqual(m, sorted(m))
        self.assertIn("e1g1", legal_moves(KIWI)); self.assertIn("e1c1", legal_moves(KIWI))
        self.assertIn("d7c8q", legal_moves(P5)); self.assertIn("d7c8n", legal_moves(P5))
        self.assertEqual(legal_moves("4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1").count("e5d6"), 1)
    def test_start(self):
        self.assertEqual([perft(START, d) for d in range(4)], [1, 20, 400, 8902])
    def test_kiwipete(self):
        self.assertEqual(perft(KIWI, 1), 48); self.assertEqual(perft(KIWI, 2), 2039)
        t = time.perf_counter(); n = perft(KIWI, 3); dt = time.perf_counter() - t
        self.assertEqual(n, 97862); self.assertLess(dt, 60)
    def test_p3_enpassant_pins(self):
        self.assertEqual([perft(P3, d) for d in (1, 2, 3, 4)], [14, 191, 2812, 43238])
    def test_p4_p5(self):
        self.assertEqual([perft(P4, d) for d in (1, 2, 3)], [6, 264, 9467])
        self.assertEqual([perft(P5, d) for d in (1, 2)], [44, 1486])
        self.assertEqual(perft(P5, 3), 62379)

if __name__ == "__main__":
    unittest.main()
