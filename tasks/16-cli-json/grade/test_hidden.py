import sys, os, unittest; sys.path.insert(0, os.getcwd())

import subprocess, json, tempfile, pathlib
def cli(*a):
    return subprocess.run([sys.executable, "stats.py", *a], capture_output=True, text=True, timeout=60)
class T(unittest.TestCase):
    def test_text_unchanged(self):
        r = cli("runs.jsonl")
        self.assertEqual(r.stdout, "3 runs, 2 ok, 1 failed\n  brief: 2 runs, avg 13.5s\n  chess: 1 runs, avg 3.0s\n")
        self.assertEqual(r.stderr, "")
    def test_json(self):
        p = pathlib.Path(tempfile.mkdtemp()) / "r.jsonl"
        p.write_text(pathlib.Path("runs.jsonl").read_text() + "\nnot json\n{\"name\": \"a\", \"status\": \"ok\", \"seconds\": 1}\n", encoding="utf-8")
        r = cli(str(p), "--json")
        d = json.loads(r.stdout)
        self.assertEqual(d, {"runs": 4, "ok": 3, "failed": 1, "by_name": {
            "a": {"runs": 1, "avg_seconds": 1.0}, "brief": {"runs": 2, "avg_seconds": 13.5}, "chess": {"runs": 1, "avg_seconds": 3.0}}})
        self.assertEqual(list(d["by_name"]), ["a", "brief", "chess"])
        self.assertIn("skipped 2 bad lines", r.stderr)
    def test_missing(self):
        r = cli("nope.jsonl")
        self.assertEqual(r.returncode, 1); self.assertTrue(r.stderr.strip())

if __name__ == "__main__":
    unittest.main()
