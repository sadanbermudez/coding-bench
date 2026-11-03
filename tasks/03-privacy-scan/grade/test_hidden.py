import sys, os, unittest; sys.path.insert(0, os.getcwd())

from router.boundary import is_private, find_private
class T(unittest.TestCase):
    def test_email(self):
        for s in ["mail ana.ruiz+cv@gmail.com now", "to j.doe@cs.uni.ac.uk", "x_y@example.org"]:
            self.assertEqual(find_private(s), ["email"], s)
    def test_iban(self):
        self.assertEqual(find_private("pay ES91 2100 0418 4502 0005 1332 please"), ["iban"])
        self.assertEqual(find_private("GB82WEST12345698765432"), ["iban"])
    def test_phone(self):
        self.assertEqual(find_private("call +44 7700 900123"), ["phone"])
        self.assertEqual(find_private("call +34-612-345-678"), ["phone"])
    def test_negative(self):
        for s in ["in 2026 it cost 4500 euros", "version 3.14 of llama", "ratio 1:400", "a@b", "+12 points"]:
            self.assertFalse(is_private(s), s)
    def test_order(self):
        self.assertEqual(find_private("+44 7700 900123 a@b.com a@b.com"), ["email", "phone"])

if __name__ == "__main__":
    unittest.main()
