[![PyPI version](https://badge.fury.io/py/chocolatine.svg)](https://badge.fury.io/py/chocolatine) ![Licence badge](https://img.shields.io/pypi/l/chocolatine) ![Python](https://img.shields.io/badge/python-3.12.2-blue.svg)
[![Actions Status](https://github.com/pe-brian/chocolatine/workflows/tests/badge.svg)](https://github.com/pe-brian/chocolatine/actions)
![Dependencies](https://img.shields.io/badge/dependencies-typeguard_choc--expr-yellowgreen)
![Downloads per month](https://img.shields.io/pypi/dm/chocolatine)
![Last commit](https://img.shields.io/github/last-commit/pe-brian/chocolatine)

# chocolatine

![Image](logo.jpg)

Chocolatine is a lightweight python library designed to easily generate SQL queries.

# Why Chocolatine ?

If you know Python programming langage but you are not at your ease with SQL (or you don't want to manage SQL queries by yourself), you can use Chocolatine to generate some SQL queries for you.
Of course, there are many other open source projects to do that, but honestly, they are more complex than most people expects from them (SQLAlchemy, Django ORM, etc...).

# Installation

```pip install chocolatine```

# Examples

__Concatenation & filtering__ :
```python
from chocolatine import Query, Col as _

query = Query().table("customer")\
               .select(
                    "customer_id",
                    (_("first_name") & ' ' & _("last_name")).upper().alias("name")
                )\
               .filter(_("first_name") >> "%E")
print(query)
```
Output :
```SQL
SELECT customer_id, UPPER(CONCAT(first_name, ' ', last_name)) AS name
FROM customer
WHERE first_name LIKE '%E'
```

__Group by, aggregation & filtering__ :
```python
from chocolatine import Query, sum, Col as _

query = Query().table("payment")\
               .select(
                    "customer_id",
                    count().alias("payment_count"),
                    sum("amount").alias(">:total_amount")
                )\
               .group_by("customer_id")\
               .filter(count() > 1 & sum("amount") > 5.00)\
               .filter(_("customer_id") != 3)
print(query)
```
Output :
```SQL
SELECT customer_id, COUNT(*) AS payment_count, SUM(amount) AS total_amount
FROM payment
WHERE customer_id != 3
GROUP BY customer_id
HAVING COUNT(*) > 1 AND SUM(amount) > 5.00
ORDER BY total_amount
```

__Join__ :
```python
from chocolatine import Query, Col as _

query = Query().table("film")\
               .select(
                    "title",
                    "film_id",
                    (_("first_name") & " " & _("last_name")).alias("name")
                )\
               .join("film_actor", "film_id")\
               .join("actor", "actor_id")\
               .build()
print(query)
```
Output :
```SQL
SELECT title, film_id, CONCAT(first_name, ' ', last_name) AS name
FROM film
INNER JOIN film_actor
USING film_id
INNER JOIN actor
USING actor_id
```

_Note : Random aliases have been used to remove ambiguity on joins clauses. You can always define your own aliases instead._

# SQL dialect

For now, Chocolatine is only designed to generate MySQL queries.
It is not excluded that in the future it will be compatible with Sqlite3, SqlServer or postgreSQL

# Basic functionnalities

- Select, Update & delete queries
- Distinct
- Names aliases
- Columns ordering
- Group by & aggregations
- Joins
- SQL functions
- Concatenations
- Unions
- Case-When

# Advanced functionnalities

- Dynamic type checking
- Use of : or @ in col or table name directly for alias
- Protection against SQL injection attacks
- Calls orders doesn't matter (except for join clauses)
- Compact or extended SQL expressions
- Whole system to deal with conditions (logical operators, boolean operators, priority order)
- Automatic handling of filter conditions to fill the having or where clause depending on the given columns
- Shortcut functions : Asc, Desc, Sum, Count, Upper, Lower, Concat, Second, Minute, Hour, Day, Month, Year
- \>: or <: at first position in column name (or alias) in select to set the ordering
- \>\> operator to perform a "like" condition on a column
- << operator to perform a "in" condition on a column
- Nested queries
- "ChocExpr" mini langage for SQL queries templating :
    - Conditions
    - Basic loops (with unpacking lists)

# To-do

- Equality evaluation in ChocExpr if statements
- Option to disable dynamic type checking (for performance concerns)
- Create queries
- SQLServer compatibility
- PostGreSQL compatibility
- SQLite3 compatibility

# Tests

```python pytest```

# Install Sakila database (mySQL) with Docker

```docker run -p 3306:3306 -d sakiladb/mysql:latest```

# Contributors

- peb-8 (main code)
- ryry-shi (testing)
