import sys, os, unittest; sys.path.insert(0, os.getcwd())

from pace import parse_time, pace_per_km, finish_time
class T(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(parse_time("1:45:30"), 6330)
        self.assertEqual(parse_time("45:30"), 2730)
        self.assertEqual(parse_time("59"), 59)
        for bad in ["1:60:00", "61:00:x", "-5", "", "1:2:3:4", "5:75"]:
            with self.assertRaises(ValueError, msg=bad):
                parse_time(bad)
    def test_pace(self):
        self.assertEqual(pace_per_km("1:45:30", 21.0975), "5:00/km")
        self.assertEqual(pace_per_km("50:00", 10), "5:00/km")
        self.assertEqual(pace_per_km("0:25:01", 5), "5:00/km")
        self.assertEqual(pace_per_km("0:25:03", 5), "5:01/km")
        with self.assertRaises(ValueError):
            pace_per_km("10:00", 0)
    def test_finish(self):
        self.assertEqual(finish_time("4:59/km", 21.0975), "1:45:08")
        self.assertEqual(finish_time("5:00", 42.195), "3:30:59")

if __name__ == "__main__":
    unittest.main()
