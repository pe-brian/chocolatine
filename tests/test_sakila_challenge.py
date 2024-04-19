from chocolatine import Query, Col as _, month, year, sum, count


def test_query_1a():
    """ How to display the first and last names of all actors from the table `actor` ? """
    assert Query(compact=False) \
        .table("actor") \
        .select("first_name", "last_name") \
        .build() == """\
SELECT first_name, last_name
FROM actor
"""


def test_query_1b():
    """ How to display the first and last name of each actor in a single column in upper case letters. Name the column `Actor Name` ? """
    assert Query(compact=False) \
        .table("actor") \
        .select((_("first_name") & " " & _("last_name")).upper().alias("actor_name")) \
        .build() == """\
SELECT UPPER(CONCAT(first_name, ' ', last_name)) AS actor_name
FROM actor
"""


def test_query_2a():
    """ How to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." ? """
    assert Query(compact=False) \
        .table("actor") \
        .select("actor_id", "first_name", "last_name") \
        .filter(_("first_name") == 'Joe') \
        .build() == """\
SELECT actor_id, first_name, last_name
FROM actor
WHERE (first_name = 'Joe')
"""


def test_query_2b():
    """ How to find all actors whose last name contain the letters `GEN` ? """
    assert Query(compact=False) \
        .table('actor')\
        .filter(_("last_name").like('%GEN%')) \
        .build() == """\
SELECT *
FROM actor
WHERE (last_name LIKE '%GEN%')
"""


def test_query_2c():
    """ How to find all actors whose last names contain the letters `LI`, ordering the rows by last name and first name ? """
    assert Query(compact=False) \
        .table("actor")\
        .select(_("last_name").order(), _("first_name").order())\
        .filter(_("last_name").like(r'%LI%'))\
        .build() == """\
SELECT last_name, first_name
FROM actor
WHERE (last_name LIKE '%LI%')
ORDER BY last_name ASC, first_name ASC
"""


def test_query_2d():
    """ Using `IN`, display the `country_id` and `country` columns of the following countries Afghanistan, Bangladesh, and China """
    assert Query(compact=False) \
        .table('country') \
        .select('country_id', 'country') \
        .filter(_('country').isin(('Afghanistan', 'Bangladesh', 'China'))) \
        .build() == """\
SELECT country_id, country
FROM country
WHERE (country IN ('Afghanistan', 'Bangladesh', 'China'))
"""


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

def test_query_4a():
    """ List the last names of actors, as well as how many actors have that last name """
    assert Query(compact=False) \
        .table("actor") \
        .select(_('last_name'), _("*").count().alias('count')) \
        .group_by("last_name") \
        .build() == """\
SELECT last_name, COUNT(*) AS count
FROM actor
GROUP BY last_name
"""


def test_query_4b():
    """ List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors """
    assert Query(compact=False) \
        .table("actor") \
        .select(_('last_name'), _("*").count().alias('count')) \
        .group_by("last_name")\
        .filter(_('*').count() > 1)\
        .build() == """\
SELECT last_name, COUNT(*) AS count
FROM actor
GROUP BY last_name
HAVING (COUNT(*) > 1)
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

def test_query_6a():
    """Use `JOIN` to display the first and last names, as well as the address, of each staff member. Use the tables `staff` and `address`:"""
    assert Query(compact=False)\
        .table("staff")\
        .select("first_name", "last_name", "address")\
        .join("address", "address_id")\
        .build() == """\
SELECT first_name, last_name, address
FROM staff
INNER JOIN address
USING address_id
"""


def test_query_6b():
    """ Use `JOIN` to display the total amount rung up by each staff member in August of 2005. Use tables `staff` and `payment` """
    assert Query(compact=False)\
        .table("staff")\
        .select("first_name", "last_name", sum("amount"))\
        .join("payment", "staff_id")\
        .filter((month("payment_date") == 8) & (year("payment_date") == 2005))\
        .group_by("staff_id")\
        .build() == """\
SELECT first_name, last_name, SUM(amount)
FROM staff
INNER JOIN payment
USING staff_id
WHERE ((MONTH(payment_date) = 8) AND (YEAR(payment_date) = 2005))
GROUP BY staff_id
"""


def test_query_6c():
    """ List each film and the number of actors who are listed for that film. Use tables `film_actor` and `film`. Use inner join """
    assert Query(compact=False)\
        .table("film")\
        .select("title", count().alias("<:actor_count"))\
        .join("film_actor", "film_id")\
        .group_by("title")\
        .build() == """\
SELECT title, COUNT(*) AS actor_count
FROM film
INNER JOIN film_actor
USING film_id
GROUP BY title
ORDER BY actor_count DESC
"""


def test_query_6d():
    """ How many copies of the film `Hunchback Impossible` exist in the inventory system? """
    assert Query(compact=False)\
        .table("film")\
        .select("title", count().alias("Number_of_copies"))\
        .filter(_("title") == "Hunchback Impossible")\
        .join("inventory", "film_id")\
        .group_by("title")\
        .build() == """\
SELECT title, COUNT(*) AS Number_of_copies
FROM film
INNER JOIN inventory
USING film_id
WHERE (title = 'Hunchback Impossible')
GROUP BY title
"""


def test_query_6e():
    """ Using the tables `payment` and `customer` and the `JOIN` command, list the total paid by each customer. List the customers """
    assert Query(compact=False)\
        .table("customer")\
        .select(">:last_name", "first_name", sum("amount").alias("total_paid_amount"))\
        .join("payment", "customer_id")\
        .group_by("last_name")\
        .build() == """\
SELECT last_name, first_name, SUM(amount) AS total_paid_amount
FROM customer
INNER JOIN payment
USING customer_id
GROUP BY last_name
ORDER BY last_name ASC
"""


def test_query_7a():
    """ The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with
        the letters `K` and `Q` have also soared in popularity. Use subqueries to display the titles of movies starting with the letters
        `K` and `Q` whose language is English. """
    assert Query(compact=False)\
        .table("film")\
        .select("title")\
        .filter(((_("title") >> "K%") | (_("title") >> "Q%")) & (_("language_id") << Query(table="language").select("language_id").filter(_("name") == "English")))\
        .build() == """\
SELECT title
FROM film
WHERE (((title LIKE 'K%') OR (title LIKE 'Q%')) AND (language_id IN (SELECT language_id FROM language WHERE (name = 'English'))))
"""


def test_query_7b():
    """Use subqueries to display all actors who appear in the film `Alone Trip"""
    assert Query(compact=False)\
        .table("actor")\
        .select("first_name", "last_name")\
        .filter(_("actor_id").isin(
            Query(table="film_actor").select("actor_id").filter(_("film_id").isin(
                Query(table="film").select("film_id").filter(_("title") == 'Alone Trip')))))\
        .build() == """\
SELECT first_name, last_name
FROM actor
WHERE (actor_id IN (SELECT actor_id FROM film_actor WHERE (film_id IN (SELECT film_id FROM film WHERE (title = 'Alone Trip')))))
"""


def test_query_7c():
    """You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian
    customers. Use joins to retrieve this information."""
    assert Query(compact=False)\
        .select("first_name", "last_name", "email")\
        .table("customer")\
        .join("address", "address_id")\
        .join("city", "city_id")\
        .join("country", "country_id")\
        .filter(_("country") == 'canada')\
        .build() == """\
SELECT first_name, last_name, email
FROM customer
INNER JOIN address
USING address_id
INNER JOIN city
USING city_id
INNER JOIN country
USING country_id
WHERE (country = 'canada')
"""


def test_query_7d():
    """Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies
    categorized as family films."""
    assert Query(compact=False)\
        .table("film")\
        .select("title", "name")\
        .join("film_category", "film_id")\
        .join("category", "category_id")\
        .filter(_('name') == 'family')\
        .build() == """\
SELECT title, name
FROM film
INNER JOIN film_category
USING film_id
INNER JOIN category
USING category_id
WHERE (name = 'family')
"""


def test_query_7e():
    """Display the most frequently rented movies in descending order.
    """
    assert Query(compact=False)\
        .table("film")\
        .select('title', count().alias('<:rentals'))\
        .join("inventory", 'film_id')\
        .join("rental", "inventory_id")\
        .group_by("title")\
        .build() == """\
SELECT title, COUNT(*) AS rentals
FROM film
INNER JOIN inventory
USING film_id
INNER JOIN rental
USING inventory_id
GROUP BY title
ORDER BY rentals DESC
"""


def test_query_7f():
    """ How much business, in dollars, each store brought in ? """
    assert Query(compact=False)\
        .table("payment")\
        .select('store_id', sum('amount').alias('revenue'))\
        .join('rental', 'rental_id')\
        .join('inventory', "inventory_id")\
        .join("store", "store_id")\
        .group_by("store_id")\
        .build() == """\
SELECT store_id, SUM(amount) AS revenue
FROM payment
INNER JOIN rental
USING rental_id
INNER JOIN inventory
USING inventory_id
INNER JOIN store
USING store_id
GROUP BY store_id
"""


def test_query_7g():
    """ How to display for each store its store ID, city, and country ? """
    assert Query(compact=False)\
        .table("store")\
        .select('store_id', 'city', 'country')\
        .join('address', 'address_id')\
        .join('city', 'city_id')\
        .join('country', 'country_id')\
        .build() == """\
SELECT store_id, city, country
FROM store
INNER JOIN address
USING address_id
INNER JOIN city
USING city_id
INNER JOIN country
USING country_id
"""


def test_query_7h():
    """List the top five genres in gross revenue in descending order. (**Hint**: you may need to use the following tables: category,
    film_category, inventory, payment, and rental.)"""
    assert Query(compact=False)\
        .table("payment")\
        .select(sum('amount').alias('total_amount'), 'name')\
        .join('rental', 'rental_id')\
        .join('inventory', 'inventory_id')\
        .join('category', 'category_id')\
        .group_by('name'), sum('amount')\
        .build() == """\
SELECT SUM(amount) AS total_amount, name
FROM payment
INNER JOIN rental
USING rental_id
INNER JOIN inventory
USING inventory_id
INNER JOIN category
USING category_id
GROUP BY name
ORDER BY total_amount DESC
"""


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
