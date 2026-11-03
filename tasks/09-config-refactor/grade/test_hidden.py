import sys, os, unittest; sys.path.insert(0, os.getcwd())

import ast, json, tempfile, pathlib
from app.config import load_config
from app.digest import digest
from app.brief import brief_header
from app.sync import batch_size
class T(unittest.TestCase):
    def tearDown(self):
        os.environ.pop("APP_CONFIG", None)
    def test_default_file(self):
        self.assertEqual(load_config()["timezone"], "Europe/London")
        self.assertEqual(digest(list(range(9))), [0, 1, 2])
        self.assertEqual(brief_header(), "Brief (Europe/London)")
        self.assertEqual(batch_size(), 6)
    def test_env_and_defaults(self):
        p = pathlib.Path(tempfile.mkdtemp()) / "c.json"; p.write_text("{}", encoding="utf-8")
        os.environ["APP_CONFIG"] = str(p)
        self.assertEqual(brief_header(), "Brief (Europe/Madrid)")
        self.assertEqual(batch_size(), 20)
        self.assertEqual(load_config(str(pathlib.Path("config.json").resolve()))["max_items"], 3)
    def test_no_duplicate_loading(self):
        for m in ("digest", "brief", "sync"):
            src = pathlib.Path("app", m + ".py").read_text(encoding="utf-8")
            names = {n.attr if isinstance(n, ast.Attribute) else n.id for n in ast.walk(ast.parse(src))
                     if isinstance(n, (ast.Attribute, ast.Name))}
            self.assertNotIn("open", names, m); self.assertNotIn("load", names, m)

if __name__ == "__main__":
    unittest.main()
