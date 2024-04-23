# chocolatine

![Image](logo.jpg)

Chocolatine is a lightweight python library designed to easily generate SQL query.

# Why Chocolatine ?

If you know Python programming langage but you are not at your ease with SQL (or you don't want to manage SQL requests by yourself), you can use Chocolatine to generate some SQL requests for you.
Of course, there are many other open source projects to do that, but honestly, they are more complex than most people expects from them (SQLAlchemy, Django ORM, etc...).

# Examples

__Concatenation & filtering__ :
```python
from chocolatine import Query, Col as _

req = Query().table("customer")\
               .select("customer_id", (_("first_name") & ' ' & _("last_name")).upper().alias(">name"))\
               .filter(_("first_name") >> "%E")
print(req)
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

req = Query().table("payment")\
               .select("customer_id", count().alias("payment_count"), sum("amount").alias("total_amount").order())\
               .group_by("customer_id")\
               .filter(count() > 1 & sum("amount") > 5.00)\
               .filter(_("customer_id") != 3)
print(req)
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

req = Query().table("film")\
               .select("title", "film_id", (_("first_name") & " " & _("last_name")).alias("name"))\
               .join("film_actor", "film_id")\
               .join("actor", "actor_id")\
               .build()
print(req)
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

- Select requests
- Distinct
- Aliases (for columns & tables)
- Ordering
- Group by
- Aggregation functions
- Joins
- SQL functions
- Concatenations

# Advanced functionnalities

- Dynamic type checking
- Use of : or @ in col or table name directly for alias
- NamedExpr value checking to prevent SQL injection attacks
- Calls orders doesn't matter (except for join clauses)
- Compact or extended SQL expressions
- Whole system to deal with conditions (logical operators, boolean operators, priority order)
- Automatic handling of filter conditions to fill the having or where clause depending on the given columns
- Automatic join condition on same name columns for both tables
- Auto-alias on join clause if needed
- Use of auto-alias on select clause if needed
- Shortcut functions : Asc, Desc, Sum, Count, Upper, Lower
- \>: or <: at first position in column name in select to set the ordering
- \>: or <: in column alias
- \>\> operator to perform a "like" condition on a column
- << operator to perform a "in" condition on a column
- Limit clause
- Using keyword
- Nested select requests
- Check conditions values
- Mini langage for SQL requests templating : Choc expr
- Choc expr : Conditions
- Choc expr : Basic loops (with unpacking lists)
- Case When
- Update requests
- Delete requests

# To-do

- Concat shortcut function
- Possibility to disable dynamic type checking (for performance concerns)
- Create requests
- Pypi package (to install with pip install)
- SQLServer compatibility
- PostGreSQL compatibility
- SQLite3 compatibility

# Tests

```python pytest```

# Install Sakila database (mySQL) with Docker

```docker run -p 3306:3306 -d sakiladb/mysql:latest```

# Use Chocolatine to directly query your mySQL database

Take a look at : `scratch.py`

# Contributors

- peb-8 (main code)
- ryry-shi (testing)
