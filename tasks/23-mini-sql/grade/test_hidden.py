import sys, os, unittest; sys.path.insert(0, os.getcwd())

import random, sqlite3
from minisql import query
NAMES = ["ana", "bo", "carla", "dev", "eli"]; CITIES = ["Madrid", "Glasgow", "Terrassa"]
def table(rnd, n):
    return [{"id": i, "name": rnd.choice(NAMES), "city": rnd.choice(CITIES), "age": rnd.randint(18, 70),
             "score": round(rnd.uniform(0, 100), 1)} for i in range(n)]
def cond(rnd, d=0):
    r = rnd.random()
    if d < 2 and r < 0.25:
        return f"({cond(rnd, d+1)} {rnd.choice(['AND', 'or'])} {cond(rnd, d+1)})"
    if d < 2 and r < 0.35:
        return f"NOT {cond(rnd, d+1)}"
    col = rnd.choice(["age", "score", "name", "city", "id"])
    op = rnd.choice(["=", "!=", "<", "<=", ">", ">=", "<>"])
    val = {"age": str(rnd.randint(18, 70)), "score": f"{rnd.uniform(0, 100):.1f}", "id": str(rnd.randint(0, 40)),
           "name": f"'{rnd.choice(NAMES)}'", "city": f"'{rnd.choice(CITIES)}'"}[col]
    return f"{col} {op} {val}" if rnd.random() < 0.8 else f"{val} {op} {col}"
def gen(rnd):
    where = f" WHERE {cond(rnd)}" if rnd.random() < 0.7 else ""
    kind = rnd.random()
    if kind < 0.45:
        cols = "*" if rnd.random() < 0.3 else ", ".join(rnd.sample(["id", "name", "city", "age", "score"], rnd.randint(1, 3)))
        order, limit = "", ""
        if rnd.random() < 0.6:
            keys = rnd.sample(["name", "city", "age", "score"], rnd.randint(1, 2))
            order = " ORDER BY " + ", ".join(k + rnd.choice(["", " ASC", " DESC", " desc"]) for k in keys) + ", id"
            if rnd.random() < 0.5:
                limit = f" LIMIT {rnd.randint(0, 8)}"
        return f"SELECT {cols} FROM people{where}{order}{limit}", bool(order)
    aggs = rnd.sample(["COUNT(*)", "count(age)", "SUM(age)", "AVG(score)", "MIN(name)", "MAX(score)", "sum(score)", "AVG(age)"], rnd.randint(1, 3))
    if kind < 0.65:
        return f"SELECT {', '.join(aggs)} FROM people{where}", True
    key = rnd.choice(["name", "city"])
    order = f" ORDER BY {key}{rnd.choice(['', ' DESC'])}" if rnd.random() < 0.6 else ""
    limit = f" LIMIT {rnd.randint(1, 4)}" if order and rnd.random() < 0.4 else ""
    return f"select {key}, {', '.join(aggs)} from people{where} group by {key}{order}{limit}", bool(order)
def norm(rows):
    return [tuple(round(v, 6) if isinstance(v, float) else v for v in r) for r in rows]
class T(unittest.TestCase):
    def test_vs_sqlite(self):
        rnd = random.Random(5)
        for trial in range(4):
            rows = table(rnd, rnd.choice([0, 7, 40]))
            con = sqlite3.connect(":memory:")
            con.execute("create table people(id integer, name text, city text, age integer, score real)")
            con.executemany("insert into people values (?,?,?,?,?)", [tuple(r.values()) for r in rows])
            for _ in range(120):
                sql, ordered = gen(rnd)
                want = norm(con.execute(sql).fetchall())
                got = norm(query(sql, {"people": rows}))
                if not ordered:
                    want, got = sorted(want, key=repr), sorted(got, key=repr)
                self.assertEqual(got, want, sql)
                if want:
                    self.assertEqual([type(v) for v in got[0]], [type(v) for v in want[0]], sql)
    def test_errors(self):
        t = {"people": [{"id": 1, "name": "a"}]}
        for bad in ["SELECT FROM people", "SELECT name people", "SELECT name FROM people WHERE", "SELECT name FROM people LIMIT x",
                    "DELETE FROM people", "SELECT name FROM people WHERE name = 'a"]:
            with self.assertRaises(ValueError, msg=bad):
                query(bad, t)

if __name__ == "__main__":
    unittest.main()
