# chocolatine

![Image](logo.jpg)

Chocolatine is a lightweight python library designed to easily generate SQL request.

# Why Chocolatine ?

If you know Python programming langage but you are not at your ease with SQL (or you don't want to manage SQL requests by yourself), you can use Chocolatine to generate some SQL requests for you.
Of course, there are many other open source projects to do that, but honestly, they are more complex than most people expects from them (SQLAlchemy, Django ORM, etc...).

# Examples

__Concatenation & filtering__ :
```python
from chocolatine import Request, Col as _

req = Request().table("customer")\
               .select("customer_id", (_("first_name") & ' ' & _("last_name")).upper().alias(">name"))\
               .filter(_("first_name").like("%E"))
print(req)
```
Output :
```SQL
SELECT customer_id, UPPER(CONCAT(first_name, ' ', last_name)) AS name FROM customer
WHERE first_name LIKE '%E'
```

__Group by, aggregation & filtering__ :
```python
from chocolatine import Request, sum, Col as _

req = Request().table("payment")\
               .select("customer_id", count().alias("payment_count"), sum("amount").alias("total_amount").order())\
               .group_by("customer_id")\
               .filter(count() > 1 & sum("amount") > 5.00)\
               .filter(_("customer_id") != 3)
print(req)
```
Output :
```SQL
SELECT customer_id, COUNT(*) AS payment_count, SUM(amount) AS total_amount FROM payment
WHERE customer_id != 3
GROUP BY customer_id
HAVING COUNT(*) > 1 AND SUM(amount) > 5.00
ORDER BY total_amount
```

__Join__ :
```python
from chocolatine import Request, Col as _

req = Request().table("film")\
               .select("title", "film_id", _("first_name") & " " & _("last_name"))\
               .join("film_actor", "film_id")\
               .join("actor", "actor_id")\
               .build()
print(req)
```
Output :
```SQL
SELECT title, jcjqtxnn.film_id, CONCAT(first_name, ' ', last_name)
FROM film AS oetjfebo
INNER JOIN film_actor AS jcjqtxnn
ON (jcjqtxnn.film_id = oetjfebo.film_id)
INNER JOIN actor AS wcgbrway
ON (wcgbrway.actor_id = jcjqtxnn.actor_id)
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
- Expr value checking to prevent SQL injection attacks
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

# To-do

- Check conditions values
- Concat shortcut function
- Possibility to disable dynamic type checking (for performance concerns)
- Implement Case-When
- Create requests
- Update requests
- Delete requests
- Pypi package (to install with pip install)
- SQLServer compatibility
- PostGreSQL compatibility
- SQLite3 compatibility

# Tests

```python pytest```

# Install Sakila database (mySQL) with Docker

```docker run -p 3306:3306 -d sakiladb/mysql:latest```

# Use Chocolatine to directly request your mySQL database

Take a look at : `scratch.py`

# Contributors

- peb-8 (main code)
- ryry-shi (testing)
