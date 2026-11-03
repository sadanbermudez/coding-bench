import unittest
from datetime import date

from units.convert import kg_to_lb, km_to_miles, lb_to_kg
from units.dates import parse_eu, week_label


class T(unittest.TestCase):
    def test_weights(self):
        self.assertEqual(lb_to_kg(225), 102.06)
        self.assertEqual(kg_to_lb(100), 220.46)

    def test_distance(self):
        self.assertEqual(km_to_miles(21.0975), 13.109)

    def test_dates(self):
        self.assertEqual(parse_eu("02/11/2026"), date(2026, 11, 2))
        self.assertEqual(parse_eu("2-1-2027"), date(2027, 1, 2))

    def test_week(self):
        self.assertEqual(week_label(date(2026, 1, 1)), "2026-W01")
        self.assertEqual(week_label(date(2027, 1, 1)), "2026-W53")
