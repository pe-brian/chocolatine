[![PyPI version](https://badge.fury.io/py/chocolatine.svg)](https://badge.fury.io/py/chocolatine)
[![Actions Status](https://github.com/pe-brian/chocolatine/workflows/tests/badge.svg)](https://github.com/pe-brian/chocolatine/actions)
![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/pypi/l/chocolatine)
![Downloads](https://img.shields.io/pypi/dm/chocolatine)
![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen)

# chocolatine

![Logo](logo.jpg)

**A Python SQL query builder that feels like writing Python, not SQL strings.**

Chocolatine lets you build complex, type-safe SQL queries programmatically — with full IDE autocompletion, runtime type checking, and zero string concatenation.

```python
from chocolatine import Query, Col as _, Window, With

# Revenue per customer with running total — all in Python
monthly = Query.get_rows(
    "orders",
    cols=[
        _("customer_id"),
        _("created_at").date_format("%Y-%m").alias("month"),
        (_("quantity") * _("unit_price")).alias("revenue"),
    ],
    groups=["customer_id", "month"]
)

With(
    ctes=[("monthly", monthly)],
    query=Query.get_rows("monthly", cols=[
        _("customer_id"),
        _("month"),
        _("revenue"),
        Window.sum(_("revenue"), partition_by=[_("customer_id")], order_by=[_("month")]).alias("running_total"),
    ])
).build()
```
```sql
WITH monthly AS (
  SELECT customer_id, DATE_FORMAT(created_at, '%Y-%m') AS month, (quantity * unit_price) AS revenue
  FROM orders GROUP BY customer_id, month
)
SELECT customer_id, month, revenue,
       SUM(revenue) OVER (PARTITION BY customer_id ORDER BY month) AS running_total
FROM monthly
```

---

## Why Chocolatine?

Most SQL builders are either too verbose (SQLAlchemy Core), too tied to an ORM (Django ORM, SQLModel), or too low-level (raw f-strings). Chocolatine sits in the middle: **lightweight, expressive, and complete**.

| Feature | Chocolatine | Raw SQL strings | SQLAlchemy Core |
|---|:---:|:---:|:---:|
| Type-safe at runtime | Yes | No | Partial |
| IDE autocompletion | Yes | No | Yes |
| No dependencies except Python | Near-zero | Yes | No |
| Window functions | Yes | Yes | Yes |
| CTEs | Yes | Yes | Yes |
| Learning curve | Low | None | High |

---

## Installation

```bash
pip install chocolatine
```

Requires Python 3.13+.

---

## Quick start

```python
from chocolatine import Query, Col as _

# SELECT
Query.get_rows("users", filters=[_("active") == 1], limit=10).build()
# SELECT * FROM users WHERE (active = 1) LIMIT 10

# INSERT
Query.insert_row("users", [_("name"), _("email")], ("Alice", "alice@example.com")).build()
# INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')

# UPDATE
Query.update_rows("users", filters=[_("id") == 1], assignations=[_("name") == "Bob"]).build()
# UPDATE users SET (name = 'Bob') WHERE (id = 1)

# DELETE
Query.delete_rows("users", filter=_("active") == 0).build()
# DELETE FROM users WHERE (active = 0)
```

---

## Core concepts

### Columns

```python
from chocolatine import Col as _

_("price")                          # price
_("u.email")                        # u.email  (table prefix)
_("amount").alias("total")          # amount AS total
_("amount:total")                   # amount AS total  (shorthand)
_("amount").sum().alias("total")    # SUM(amount) AS total
_("name").upper()                   # UPPER(name)
_("created_at").date_format("%Y-%m")# DATE_FORMAT(created_at, '%Y-%m')
```

### Filtering

Filters are combined with `AND` automatically when chained:

```python
q = Query.get_rows("users")
q.filter(_("age") > 18)
q.filter(_("city") == "Paris")
q.filter(_("active") == 1)
# WHERE (((age > 18) AND (city = 'Paris')) AND (active = 1))
```

Use operators directly for more control:

```python
from chocolatine import Col as _

_("age").between(18, 65)                        # age BETWEEN 18 AND 65
_("email").is_null()                             # email IS NULL
_("status") << ("active", "pending")            # status IN ('active', 'pending')
_("name") >> "%alice%"                          # name LIKE '%alice%'
~_("email").is_null()                            # NOT (email IS NULL)
(_("age") > 18) & (_("city") == "Paris")        # (age > 18) AND (city = 'Paris')
(_("tier") == "gold") | (_("tier") == "silver") # (tier = 'gold') OR (tier = 'silver')
```

### Arithmetic expressions

```python
(_("qty") * _("unit_price")).alias("total")          # (qty * unit_price) AS total
(_("revenue") - _("cost")).alias("margin")           # (revenue - cost) AS margin
(_("revenue") / _("sessions") * 100).alias("rate")  # ((revenue / sessions) * 100) AS rate
_("stock") + 1                                        # (stock + 1)

# Use in filters
Query.get_rows("orders", filters=[_("qty") * _("unit_price") > 500])
# WHERE ((qty * unit_price) > 500)
```

### Joins

```python
Query.get_rows(
    "orders o",
    cols=[_("o.id"), _("c.name"), _("c.email")],
    joins=[
        ("customers c", _("c.id") == _("o.customer_id")),
        ("order_items oi", _("oi.order_id") == _("o.id"), JoinType.Left),
    ]
)
```

### Aggregations

```python
from chocolatine import count, sum, Col as _

Query.get_rows(
    "orders",
    cols=[
        _("customer_id"),
        count().alias("nb_orders"),
        _("amount").sum().alias("total"),
        _("amount").average().alias("avg"),
    ],
    groups=["customer_id"],
    filters=[_("amount").sum() > 100]   # routed to HAVING automatically
)
# SELECT customer_id, COUNT(*) AS nb_orders, SUM(amount) AS total, AVG(amount) AS avg
# FROM orders GROUP BY customer_id HAVING (SUM(amount) > 100)
```

### String functions

```python
_("name").upper()                       # UPPER(name)
_("name").lower()                       # LOWER(name)
_("name").trim()                        # TRIM(name)
_("name").length()                      # LENGTH(name)
_("name").replace("foo", "bar")         # REPLACE(name, 'foo', 'bar')
_("bio").substring(1, 255)             # SUBSTRING(bio, 1, 255)
_("code").lpad(10, "0")                # LPAD(code, 10, '0')
_("name").left(3)                      # LEFT(name, 3)
_("score").round(2)                    # ROUND(score, 2)
_("created_at").date_format("%Y-%m")   # DATE_FORMAT(created_at, '%Y-%m')
_("password").md5()                    # MD5(password)

# Concatenation
_("first_name") & " " & _("last_name") # CONCAT(first_name, ' ', last_name)
```

### CASE / WHEN

```python
from chocolatine import When, ColWhen, Col as _

# Condition-based
When(
    (_("score") >= 90, _("score") >= 70, _("score") >= 50),
    ("A", "B", "C"),
    else_returned_val="F",
    compact=True
)
# CASE WHEN (score >= 90) THEN 'A' WHEN (score >= 70) THEN 'B' ... ELSE 'F' END

# Value-based
ColWhen("status", ("active", "pending"), ("Active", "Pending"), else_returned_val="Other")
# CASE status WHEN 'active' THEN 'Active' WHEN 'pending' THEN 'Pending' ELSE 'Other' END
```

### COALESCE

```python
from chocolatine import Coalesce, Col as _

Coalesce(_("phone"), _("mobile"), "N/A").alias("contact")
# COALESCE(phone, mobile, 'N/A') AS contact

Coalesce(_("discount") * _("price"), 0).alias("rebate")
# COALESCE((discount * price), 0) AS rebate
```

### EXISTS / NOT EXISTS

```python
from chocolatine import Exists, Query, Col as _

subquery = Query.get_rows("orders", filters=[_("customer_id") == _("c.id")])

Query.get_rows("customers c", filters=[Exists(subquery)])
# SELECT * FROM customers c WHERE EXISTS (SELECT * FROM orders WHERE (customer_id = c.id))

Query.get_rows("customers c", filters=[~Exists(subquery)])
# SELECT * FROM customers c WHERE NOT EXISTS (...)
```

### Window functions

```python
from chocolatine import Window, Col as _

Window.row_number(partition_by=[_("dept")], order_by=[_("salary").desc()]).alias("rn")
# ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn

Window.sum(_("amount"), partition_by=[_("dept")]).alias("dept_total")
# SUM(amount) OVER (PARTITION BY dept) AS dept_total

Window.lag(_("salary"), offset=1, order_by=[_("hire_date")])
# LAG(salary, 1) OVER (ORDER BY hire_date)

Window.ntile(4, order_by=[_("score").desc()])
# NTILE(4) OVER (ORDER BY score DESC)
```

Available: `row_number`, `rank`, `dense_rank`, `ntile`, `cume_dist`, `percent_rank`, `sum`, `avg`, `count`, `min`, `max`, `lag`, `lead`, `first_value`, `last_value`.

### CTEs (WITH)

```python
from chocolatine import With, Query, Col as _

active_users = Query.get_rows("users", filters=[_("active") == 1])
recent_orders = Query.get_rows("orders", filters=[_("created_at") > "2024-01-01"])

With(
    ctes=[
        ("active_users", active_users),
        ("recent_orders", recent_orders),
    ],
    query=Query.get_rows("active_users",
        joins=[("recent_orders", _("recent_orders.user_id") == _("active_users.id"))]
    )
).build()
# WITH active_users AS (...), recent_orders AS (...) SELECT * FROM active_users JOIN ...

# Recursive CTE
With(
    ctes=[("org", base_query.union_all(recursive_query))],
    query=Query.get_rows("org"),
    recursive=True
)
# WITH RECURSIVE org AS (...) SELECT * FROM org
```

### UNION / UNION ALL

```python
Query.get_rows("customers").union(Query.get_rows("prospects")).build()
# SELECT * FROM customers UNION SELECT * FROM prospects

Query.get_rows("active").union_all(Query.get_rows("archived")).build()
# SELECT * FROM active UNION ALL SELECT * FROM archived
```

### DDL

```python
from chocolatine import Query, Col as _, SqlType

# CREATE TABLE
Query.create_table("users", cols=[
    _("email",      type=SqlType.String,  not_null=True, unique=True),
    _("name",       type=SqlType.String,  not_null=True),
    _("score",      type=SqlType.Integer, default=0),
    _("created_at", type=SqlType.DateTime),
], auto_id=True)
# CREATE TABLE users (id MEDIUMINT NOT NULL AUTO_INCREMENT, email VARCHAR(255) NOT NULL UNIQUE, ...)

# ALTER TABLE
Query.add_col("users", Col("country", type=SqlType.String), after="name")
Query.rename_col("users", "email", "email_address")
Query.drop_col("users", "legacy_field")

# DROP / TRUNCATE
Query.drop_table("users")
Query.truncate("users")
```

### INSERT ON DUPLICATE KEY UPDATE

```python
Query.insert_row("products", [_("sku"), _("name"), _("price")], ("ABC", "Widget", 9.99)) \
    .on_duplicate_key_update(_("price") == 9.99, _("updated_at") == "NOW()")
# INSERT INTO products (sku, name, price) VALUES ('ABC', 'Widget', 9.99)
# ON DUPLICATE KEY UPDATE (price = 9.99), (updated_at = 'NOW()')
```

### Compact vs extended output

```python
q = Query.get_rows("users", compact=False, filters=[_("active") == 1])
print(q.build())
# SELECT *
# FROM users
# WHERE (active = 1)

q.compact = True   # propagates to all sub-expressions
print(q.build())
# SELECT * FROM users WHERE (active = 1)
```

---

## Full feature list

**Query types:** SELECT, INSERT, UPDATE, DELETE, CREATE TABLE, ALTER TABLE (add/rename/change/drop column), DROP TABLE, TRUNCATE

**Filtering:** WHERE, HAVING (auto-routed), IS NULL, IS NOT NULL, BETWEEN, IN, LIKE, EXISTS, NOT EXISTS, AND, OR, NOT

**Expressions:** arithmetic (`+`, `-`, `*`, `/`, `%`), string functions, date functions, multi-arg functions, COALESCE, CASE/WHEN, subqueries

**Aggregations:** COUNT, COUNT(DISTINCT), SUM, AVG, MIN, MAX + GROUP BY + HAVING

**Window functions:** ROW_NUMBER, RANK, DENSE_RANK, NTILE, CUME_DIST, PERCENT_RANK, SUM, AVG, COUNT, MIN, MAX, LAG, LEAD, FIRST_VALUE, LAST_VALUE

**Set operations:** UNION, UNION ALL

**CTEs:** WITH, WITH RECURSIVE (multiple CTEs supported)

**DDL constraints:** NOT NULL, UNIQUE, DEFAULT, AUTO_INCREMENT primary key

**Other:** JOINs (INNER/LEFT/RIGHT/FULL), ORDER BY, LIMIT, OFFSET, DISTINCT, aliases, table prefixes, compact/extended rendering

---

## SQL dialect

Chocolatine currently targets **MySQL**. Most queries are compatible with MariaDB. PostgreSQL and SQLite support is not guaranteed for dialect-specific features (e.g., `MEDIUMINT`, `DATE_FORMAT`).

---

## Development

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=chocolatine --cov-report=term-missing
```

330 tests, 99% coverage.

---

## Related

- [choc-expr](https://github.com/pe-brian/choc-expr) — the lightweight expression templating engine powering Chocolatine

---

## Contributors

- [pe-brian](https://github.com/pe-brian) — author
- [ryry-shi](https://github.com/ryry-shi) — testing
