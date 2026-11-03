import sys, os, unittest; sys.path.insert(0, os.getcwd())

import subprocess
class T(unittest.TestCase):
    def test_cli(self):
        r = subprocess.run([sys.executable, "-m", "notes", "stats", "sample"], capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.strip(), "2 notes, 8 words, tags: ai, chess")
    def test_imports(self):
        from notes.models import Note
        from notes.storage import load_folder, slugify
        self.assertEqual(Note(title="Hello, World!").slug, "hello-world")
        self.assertEqual(slugify(" A  b "), "a-b")

if __name__ == "__main__":
    unittest.main()
