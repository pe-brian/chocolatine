from chocolatine import Request, Col, Table, JoinType, Operator, Condition
from chocolatine.shortcut import count


def test_request_1a():
    """ Display the first and last names of all actors from the table `actor` """
    assert Request(compact=False) \
        .table("actor") \
        .select("first_name", "last_name") \
        .build() == """\
SELECT first_name, last_name
FROM actor\
"""


def test_request_1b():
    """ Display the first and last name of each actor in a single column in upper case letters. Name the column `Actor Name` """
    assert Request(compact=False) \
        .table("actor") \
        .select((Col("first_name") & " " & Col("last_name")).upper().alias("actor_name")) \
        .build() == """\
SELECT UPPER(CONCAT(first_name, ' ', last_name)) AS actor_name
FROM actor\
"""


def test_request_2a():
    """ You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is 
        one query would you use to obtain this information? """
    assert Request(compact=False) \
        .table("actor") \
        .select("actor_id", "first_name", "last_name") \
        .filter(Col("first_name") == 'Joe') \
        .build() == """\
SELECT actor_id, first_name, last_name
FROM actor
WHERE (first_name = 'Joe')\
"""

def test_request_2b():
   """ Find all actors whose last name contain the letters `GEN`."""
   assert Request(compact=False) \
        .table('actor')\
        .filter(Col("last_name").like('%GEN%')) \
        .build() == """\
SELECT *
FROM actor
WHERE (last_name LIKE '%GEN%')\
"""
# --'WHERE last_name LIKE '%GEN%'\

# error


def test_request_2c():
    """Find all actors whose last names contain the letters `LI`. This time, order the rows by last name and first name, in that 
        order:"""
        
    assert Request(compact=False) \
        .table("actor")\
        .select("last_name","first_name")\
        .filter(Col("last_name").like(r'%LI%'))\
        .build() == """\
SELECT last_name, first_name
FROM actor
WHERE (last_name LIKE '%LI%')\
"""


def test_request_2d():
    """ Using `IN`, display the `country_id` and `country` columns of the following countries 
        Afghanistan, Bangladesh, and China """
    assert Request(compact=False) \
        .table('country') \
        .select('country_id', 'country') \
        .filter(Col('country').isin('Afghanistan', 'Bangladesh', 'China')) \
        .build() == """\
SELECT country_id, country
FROM country
WHERE (country IN ('Afghanistan', 'Bangladesh', 'China'))\
"""
# error
# problème de paranthèse


# 3a. Add a `middle_name` column to the table `actor`. Position it between `first_name` and `last_name`. Hint: you will need to
# specify the data type.

#   ALTER TABLE actor
# 	ADD middle_name VARCHAR(25) AFTER first_name;

# 3b. You realize that some of these actors have tremendously long last names. Change the data type of the `middle_name` column to
# `blobs`.

#   ALTER TABLE actor
# 	MODIFY COLUMN middle_name blob;

# 3c. Now delete the `middle_name` column.
#   ALTER TABLE actor
# 	DROP COLUMN middle_name;

def test_request_4a():
    """List the last names of actors, as well as how many actors have that last name."""
    assert Request(compact=False) \
        .table("actor") \
        .select(Col('last_name'), Col("*").count().alias('count')) \
        .group_by("last_name") \
        .build() == """\
SELECT last_name, COUNT(*) AS count
FROM actor
GROUP BY last_name\
"""

#   
def test_request_4b():
        """4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least
        two actors."""
        assert Request(compact=False) \
        .table("actor") \
        .select(Col('last_name'), Col("*").count().alias('count')) \
        .group_by("last_name")\
        .filter(Col('*').count() > 1)\
        .build() == """\
SELECT last_name, COUNT(*) AS count
FROM actor
GROUP BY last_name
HAVING (COUNT(*) > 1)\
"""


# 4c. Oh, no! The actor `HARPO WILLIAMS` was accidentally entered in the `actor` table as `GROUCHO WILLIAMS`, the name of Harpo's
# second cousin's husbands yoga teacher. Write a query to fix the record.

#   UPDATE actor
#   SET first_name ='HARPO'
#   WHERE (first_name ='GROUCHO' AND last_name = 'WILLIAMS');

# 4d. Perhaps we were too hasty in changing `GROUCHO` to `HARPO`. It turns out that `GROUCHO` was the correct name after all! In a
# single query, if the first name of the actor is currently `HARPO`, change it to `GROUCHO`. Otherwise, change the first name to
# `MUCHO GROUCHO`, as that is exactly what the actor will be with the grievous error. BE CAREFUL NOT TO CHANGE THE FIRST NAME OF
# EVERY ACTOR TO `MUCHO GROUCHO`, HOWEVER! (Hint: update the record using a unique identifier.)

#   UPDATE actor
#   SET first_name =
#   CASE WHEN first_name = 'HARPO'
#   THEN 'GROUCHO'
#   ELSE 'MUCHO GROUCHO'
#   END
#   WHERE actor_id = 172;

# 5a. You cannot locate the schema of the `address` table. Which query would you use to re-create it?

#   SHOW CREATE TABLE address;

def test_request_6a():
    """a. Use `JOIN` to display the first and last names, as well as the address, of each staff member. Use the tables `staff` and
    `address`:"""
    assert Request(compact=False)\
        .table("staff", "s")\
        .select("s.first_name, s.last_name, a.address")\
        .join(Table("address", "a"), JoinType.Inner, Col("address_id") == Col("address_id"))\
        .build() == """\
SELECT s.first_name, s.last_name, a.address
FROM staff AS s
INNER JOIN address AS a
ON (s.address_id = a.address_id)\
"""



#   
#   
#   USING (film_id)
#   WHERE title = 'Hunchback Impossible'
#   GROUP BY title;

# 6e. Using the tables `payment` and `customer` and the `JOIN` command, list the total paid by each customer. List the customers
# alphabetically by last name:

# SELECT c.last_name, c.first_name, SUM(p.amount) AS 'Total Amount Paid'
# FROM customer c
# INNER JOIN payment p 
# ON (c.customer_id = p.customer_id)
# GROUP BY c.last_name
# ORDER BY c.last_name;

# 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with
# the letters `K` and `Q` have also soared in popularity. Use subqueries to display the titles of movies starting with the letters
# `K` and `Q` whose language is English.

#   SELECT title
#   FROM film
#   WHERE title LIKE 'K%'
#   OR title LIKE 'Q%'
#   AND language_id IN
#   (SELECT language_id
#   FROM language
#   WHERE name = 'English'
#   );

# 7b. Use subqueries to display all actors who appear in the film `Alone Trip`.

#   SELECT first_name, last_name
#   FROM actor
#   WHERE actor_id IN
#   (SELECT actor_id
#   FROM film_actor
#   WHERE film_id IN
#   (SELECT film_id
#   FROM film
#   WHERE title = 'Alone Trip'));

# 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian
# customers. Use joins to retrieve this information.

#   SELECT c.first_name, c.last_name, c.email
#   FROM customer c
#   JOIN address a ON (c.address_id = a.address_id)
#   JOIN city ci ON (a.city_id = ci.city_id)
#   JOIN country ctr ON (ci.country_id = ctr.country_id)
#   WHERE ctr.country = 'canada';

# 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies
# categorized as family films.

#   SELECT title, c.name
#   FROM film f
#   JOIN film_category fc
#   ON (f.film_id = fc.film_id)
#   JOIN category c
#   ON (c.category_id = fc.category_id)
#   WHERE name = 'family';

# 7e. Display the most frequently rented movies in descending order.

#   SELECT title, COUNT(title) as 'Rentals'
#   FROM film
#   JOIN inventory
#   ON (film.film_id = inventory.film_id)
#   JOIN rental
#   ON (inventory.inventory_id = rental.inventory_id)
#   GROUP by title
#   ORDER BY rentals desc;

# 7f. Write a query to display how much business, in dollars, each store brought in.

#   SELECT s.store_id, SUM(amount) AS 'Revenue'
#   FROM payment p
#   JOIN rental r
#   ON (p.rental_id = r.rental_id)
#   JOIN inventory i
#   ON (i.inventory_id = r.inventory_id)
#   JOIN store s
#   ON (s.store_id = i.store_id)
#   GROUP BY s.store_id;

# 7g. Write a query to display for each store its store ID, city, and country.

#   SELECT store_id, city, country
#   FROM store s
#   JOIN address a
#   ON (s.address_id = a.address_id)
#   JOIN city cit
#   ON (cit.city_id = a.city_id)
#   JOIN country ctr
#   ON(cit.country_id = ctr.country_id);	


# 7h. List the top five genres in gross revenue in descending order. (**Hint**: you may need to use the following tables: category,
# film_category, inventory, payment, and rental.)

#   SELECT SUM(amount) AS 'Total Sales', c.name AS 'Genre'
#   FROM payment p
#   JOIN rental r
#   ON (p.rental_id = r.rental_id)
#   JOIN inventory i
#   ON (r.inventory_id = i.inventory_id)
#   JOIN film_category fc
#   ON (i.film_id = fc.film_id)
#   JOIN category c
#   ON (fc.category_id = c.category_id)
#   GROUP BY c.name
#   ORDER BY SUM(amount) DESC;

# 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. Use the
# solution from the problem above to create a view. If you havent solved 7h, you can substitute another query to create a view.

#   CREATE VIEW top_five_genres AS
#   SELECT SUM(amount) AS 'Total Sales', c.name AS 'Genre'
#   FROM payment p
#   JOIN rental r
#   ON (p.rental_id = r.rental_id)
#   JOIN inventory i
#   ON (r.inventory_id = i.inventory_id)
#   JOIN film_category fc
#   ON (i.film_id = fc.film_id)
#   JOIN category c
#   ON (fc.category_id = c.category_id)
#   GROUP BY c.name
#   ORDER BY SUM(amount) DESC
#   LIMIT 5;

# 8b. How would you display the view that you created in 8a?

#   SELECT * 
#   FROM top_five_genres;

# 8c. You find that you no longer need the view `top_five_genres`. Write a query to delete it.

#   DROP VIEW top_five_genres;