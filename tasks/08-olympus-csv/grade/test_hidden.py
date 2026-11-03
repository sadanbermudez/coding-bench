import sys, os, unittest; sys.path.insert(0, os.getcwd())

from datetime import date
from olympus.importer import load_sets
class T(unittest.TestCase):
    def test_comma(self):
        r = load_sets("date,exercise,reps,weight_kg\n2026-10-01, Squat ,5,100.5\n")
        self.assertEqual(r, [{"date": date(2026,10,1), "exercise": "Squat", "reps": 5, "weight_kg": 100.5}])
    def test_semicolon(self):
        t = "\ufeffdate;exercise;reps;weight_kg\n\n2026-10-02;Press banca;8;72,5\n2026-10-02;Dominadas;6;0\n\n"
        r = load_sets(t)
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0]["weight_kg"], 72.5); self.assertEqual(r[0]["exercise"], "Press banca")
        self.assertEqual(r[1]["weight_kg"], 0.0); self.assertEqual(r[0]["date"], date(2026,10,2))
    def test_quoted_name_with_comma(self):
        r = load_sets('date,exercise,reps,weight_kg\n2026-10-03,"Row, cable",10,40\n')
        self.assertEqual(r[0]["exercise"], "Row, cable")

if __name__ == "__main__":
    unittest.main()
