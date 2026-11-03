import sys, os, unittest; sys.path.insert(0, os.getcwd())

from validate import validate
S = {"type": "object", "required": ["fen", "depth"], "additionalProperties": False, "properties": {
    "fen": {"type": "string", "minLength": 10},
    "depth": {"type": "integer", "minimum": 1, "maximum": 30},
    "side": {"enum": ["white", "black"]},
    "moves": {"type": "array", "items": {"type": "object", "required": ["uci"], "properties": {"uci": {"type": "string", "maxLength": 5}}}},
    "score": {"type": "number"}, "ok": {"type": "boolean"}, "note": {"type": "null"}}}
def paths(errs): return sorted(e.split(":")[0] for e in errs)
class T(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate({"fen": "x" * 12, "depth": 5, "side": "white", "score": 1, "ok": True, "note": None,
                                   "moves": [{"uci": "e2e4"}]}, S), [])
    def test_many(self):
        e = validate({"fen": "short", "depth": 0, "side": "red", "extra": 1,
                      "moves": [{"uci": "e2e4"}, {}, {"uci": "e7e8q+x"}, 5]}, S)
        self.assertEqual(paths(e), sorted(["$.fen", "$.depth", "$.side", "$.extra", "$.moves[1]", "$.moves[2].uci", "$.moves[3]"]))
    def test_types(self):
        self.assertEqual(paths(validate({"fen": "x" * 12, "depth": True}, S)), ["$.depth"])
        self.assertEqual(paths(validate({"fen": "x" * 12, "depth": 2.5}, S)), ["$.depth"])
        self.assertEqual(validate({"fen": "x" * 12, "depth": 3, "score": 2}, S), [])
        self.assertEqual(paths(validate({"fen": "x" * 12, "depth": 3, "score": False}, S)), ["$.score"])
        self.assertEqual(paths(validate([], S)), ["$"])
        self.assertEqual(len(validate("x", {"type": "integer", "minimum": 3})), 1)
    def test_missing(self):
        self.assertEqual(paths(validate({}, S)), ["$", "$"])

if __name__ == "__main__":
    unittest.main()
