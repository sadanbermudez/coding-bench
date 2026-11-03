import sys, os, unittest; sys.path.insert(0, os.getcwd())

import sqlite3, tempfile, pathlib
from migrate import migrate
def mk(files):
    d = pathlib.Path(tempfile.mkdtemp())
    for n, s in files.items(): (d / n).write_text(s, encoding="utf-8")
    return d
class T(unittest.TestCase):
    def test_order_idempotent(self):
        d = mk({"010_c.sql": "ALTER TABLE runs ADD COLUMN c TEXT;", "2_b.sql": "CREATE INDEX ix ON runs(name);",
                "001_a.sql": "CREATE TABLE runs(name TEXT);", "notes.txt": "x", "draft.sql": "garbage"})
        db = str(d / "x.db")
        self.assertEqual(migrate(db, str(d)), ["001_a.sql", "2_b.sql", "010_c.sql"])
        self.assertEqual(migrate(db, str(d)), [])
        con = sqlite3.connect(db)
        self.assertEqual([r[0] for r in con.execute("select version from schema_version order by version")], [1, 2, 10])
        con.close()
    def test_failure(self):
        d = mk({"001_a.sql": "CREATE TABLE runs(name TEXT);",
                "002_bad.sql": "CREATE TABLE t2(x INT); INSERT INTO nope VALUES(1);"})
        db = str(d / "x.db")
        with self.assertRaises(Exception) as cm:
            migrate(db, str(d))
        self.assertIn("002_bad.sql", str(cm.exception))
        con = sqlite3.connect(db)
        tables = {r[0] for r in con.execute("select name from sqlite_master where type='table'")}
        self.assertIn("runs", tables); self.assertNotIn("t2", tables)
        self.assertEqual([r[0] for r in con.execute("select version from schema_version")], [1])
        con.close()
    def test_duplicate(self):
        d = mk({"001_a.sql": "CREATE TABLE a(x);", "01_b.sql": "CREATE TABLE b(x);"})
        with self.assertRaises(ValueError):
            migrate(str(d / "x.db"), str(d))
        con = sqlite3.connect(str(d / "x.db"))
        self.assertNotIn("a", {r[0] for r in con.execute("select name from sqlite_master")})
        con.close()

if __name__ == "__main__":
    unittest.main()
