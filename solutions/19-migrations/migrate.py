import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

PAT = re.compile(r"^(\d+)_.+\.sql$")


def migrate(db_path, migrations_dir):
    found = {}
    for p in Path(migrations_dir).iterdir():
        m = PAT.match(p.name)
        if m:
            n = int(m.group(1))
            if n in found:
                raise ValueError(f"duplicate migration number {n}")
            found[n] = p
    con = sqlite3.connect(db_path, isolation_level=None)
    try:
        con.execute("CREATE TABLE IF NOT EXISTS schema_version(version INTEGER PRIMARY KEY, name TEXT, applied_at TEXT)")
        done = {r[0] for r in con.execute("SELECT version FROM schema_version")}
        applied = []
        for n in sorted(found):
            if n in done:
                continue
            p = found[n]
            try:
                con.execute("BEGIN")
                for stmt in [s for s in p.read_text(encoding="utf-8").split(";") if s.strip()]:
                    con.execute(stmt)
                con.execute("INSERT INTO schema_version VALUES (?,?,?)", (n, p.name, datetime.now(timezone.utc).isoformat()))
                con.execute("COMMIT")
            except Exception as e:
                con.execute("ROLLBACK")
                raise RuntimeError(f"{p.name} failed: {e}") from e
            applied.append(p.name)
        return applied
    finally:
        con.close()
