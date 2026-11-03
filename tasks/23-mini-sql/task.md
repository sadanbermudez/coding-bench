Write `minisql.py` with `query(sql, tables) -> list[tuple]`: a tiny SQL engine over in-memory tables (`tables` maps a table name to a list of dicts, all with the same keys in the same order; values are int, float or str, never None). Do not use sqlite3 or any library. Results must match what SQLite returns for the same data and query. Supported (keywords case-insensitive):

```
SELECT <items> FROM <table> [WHERE <cond>] [GROUP BY <col>] [ORDER BY <col> [ASC|DESC] {, <col> [ASC|DESC]}] [LIMIT <int>]
<items> := * | <item> {, <item>}
<item>  := <col> | COUNT(*) | COUNT(<col>) | SUM(<col>) | AVG(<col>) | MIN(<col>) | MAX(<col>)
<cond>  := comparisons <operand> (= | != | <> | < | <= | > | >=) <operand>, combined with AND, OR, NOT and parentheses
<operand> := <col> | integer | decimal number | 'string' (no escapes)
```

`*` returns columns in the table's key order. With aggregates and no GROUP BY, return exactly one row (on no matching rows COUNT is 0 and the others are None). With GROUP BY, return one row per group; only the group column and aggregates are selected. AVG always returns a float; SUM/MIN/MAX of ints return ints. ORDER BY may name any table column (or the group column when grouping). NOT binds tighter than AND, AND tighter than OR. Malformed SQL raises ValueError.
