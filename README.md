# sqlens

A Python library that parses and visualizes query execution plans from Postgres and SQLite in a human-readable format.

---

## Installation

```bash
pip install sqlens
```

---

## Usage

```python
import sqlens

# PostgreSQL
import psycopg2

conn = psycopg2.connect("dbname=mydb user=postgres")
plan = sqlens.explain(conn, "SELECT * FROM orders JOIN users ON orders.user_id = users.id")
print(plan.visualize())

# SQLite
import sqlite3

conn = sqlite3.connect("mydb.sqlite")
plan = sqlens.explain(conn, "SELECT * FROM products WHERE price > 100")
print(plan.visualize())
```

**Example output:**

```
Seq Scan on orders  (cost=0.00..45.00 rows=1000)
  → Hash Join  (cost=12.50..89.30 rows=500)
      → Index Scan on users using users_pkey  (cost=0.00..8.27 rows=227)
```

You can also access the parsed plan tree directly:

```python
node = plan.root
print(node.node_type)      # "Hash Join"
print(node.total_cost)     # 89.30
print(node.children)       # list of child nodes
```

---

## Features

- Supports **PostgreSQL** (via `EXPLAIN` / `EXPLAIN ANALYZE`) and **SQLite** (`EXPLAIN QUERY PLAN`)
- Clean, tree-style visualization in the terminal
- Programmatic access to plan nodes and cost estimates
- Works with any PEP 249-compliant database connection

---

## License

MIT © sqlens contributors