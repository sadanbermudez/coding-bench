import sys, os, unittest; sys.path.insert(0, os.getcwd())

import tempfile, pathlib
from checklinks import broken_links
class T(unittest.TestCase):
    def test_vault(self):
        r = pathlib.Path(tempfile.mkdtemp())
        (r / "07 - Map").mkdir(); (r / "docs").mkdir()
        (r / "Home.md").write_text("[[Map]] [[map|alias]] [[Missing]] [[Map#Areas]]\n[x](docs/My%20Note.md) [y](docs/nope.md) [z](https://a.b) [w](#top)\n", encoding="utf-8")
        (r / "07 - Map" / "Map.md").write_text("[up](../Home.md#top) [bad](Home.md)\n```\n[[InCode]]\n```\n`[[Inline]]` [[Ghost]]\n", encoding="utf-8")
        (r / "docs" / "My Note.md").write_text("[[home]]", encoding="utf-8")
        self.assertEqual(broken_links(str(r)), [
            ("07 - Map/Map.md", "Ghost"), ("07 - Map/Map.md", "Home.md"),
            ("Home.md", "Missing"), ("Home.md", "docs/nope.md")])

if __name__ == "__main__":
    unittest.main()
