import sys, os, unittest; sys.path.insert(0, os.getcwd())

from datetime import date
from units.convert import kg_to_lb, km_to_miles, lb_to_kg
from units.dates import parse_eu, week_label
import pathlib, hashlib
class T(unittest.TestCase):
    def test_all(self):
        self.assertEqual(lb_to_kg(225), 102.06); self.assertEqual(kg_to_lb(100), 220.46); self.assertEqual(lb_to_kg(1), 0.45)
        self.assertEqual(km_to_miles(21.0975), 13.109)
        self.assertEqual(parse_eu("02/11/2026"), date(2026, 11, 2)); self.assertEqual(parse_eu("31-12-2026"), date(2026, 12, 31))
        self.assertEqual(week_label(date(2026, 1, 1)), "2026-W01"); self.assertEqual(week_label(date(2027, 1, 1)), "2026-W53")
        self.assertEqual(week_label(date(2026, 11, 2)), "2026-W45")
    def test_tests_untouched(self):
        src = pathlib.Path("tests/test_units.py").read_text(encoding="utf-8").replace("\r\n", "\n")
        self.assertEqual(hashlib.sha256(src.encode()).hexdigest(), "1c5000894b8b1f07f2cba60212809d3b520fae3c9669a2e20bf0090866ef2b84")

if __name__ == "__main__":
    unittest.main()
