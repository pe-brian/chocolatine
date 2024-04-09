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
               .select("customer_id", (_("first_name") & ' ' & _("last_name")).upper().alias("name"))\
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
               .select(
                    "customer_id",
                    count().alias("payment_count"),
                    sum("amount").alias("total_amount").order()\
               )\
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

req = Request().table("film:f")\
               .select("f.title", _("a.first_name") & " " & _("a.last_name"))\
               .join("film_actor:fa", _("fa.film_id") == _("f.film_id"))\
               .join("actor:a", _("a.actor_id") == _("fa.actor_id"))\
               .build()
print(req)
```
Output :
```SQL
SELECT f.title, CONCAT(a.first_name, ' ', a.last_name) FROM film AS f
INNER JOIN film_actor AS fa ON (fa.film_id = f.film_id)
INNER JOIN actor AS a ON (a.actor_id = fa.actor_i)
```

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
- Calls orders doesn't matter (Chocolatine automatically adjust the SQL requests clauses order for you)
- Compact or extended SQL expressions
- Whole system to deal with conditions (logical operators, boolean operators, priority order)
- Automatic handling of filter conditions to fill the having or where clause depending on the given columns

# To-do

- Check conditions values
- Possibility to disable dynamic type checking (for performance concerns)
- Implement Case-When
- Auto ambiguity removing on select columns names (after a join clause for example)
- Automatic join conditions on same name columns for both tables
- Create requests
- Update requests
- Delete requests
- Pypi package (to install with pip install)

# Tests

```python pytest```

# Install Sakila database (mySQL) with Docker

```docker run -p 3306:3306 -d sakiladb/mysql:latest```

# Use Chocolatine to directly request your mySQL database

Take a look at : `scratch.py`

# Contributors

- peb-8 (main code)
- ryry-shi (testing)
