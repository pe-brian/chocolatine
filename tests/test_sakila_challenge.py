from chocolatine import Query, Col as _, month, year, sum, count, QueryMode, When, View, ViewMode


def test_query_1a():
    """ How to display the first and last names of all actors from the table `actor` ? """
    assert str(Query(
        compact=False,
        table="actor",
        cols=("first_name", "last_name"),
    )) == """\
SELECT first_name, last_name
FROM actor
"""


def test_query_1b():
    """ How to display the first and last name of each actor in a single column in upper case letters (name the column `actor_name`) ? """
    assert str(Query(
        compact=False,
        table="actor",
        cols=((_("first_name") & " " & _("last_name")).upper().alias("actor_name"),)
    )) == """\
SELECT UPPER(CONCAT(first_name, ' ', last_name)) AS actor_name
FROM actor
"""


def test_query_2a():
    """ How to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." ? """
    assert str(Query(
        compact=False,
        table="actor",
        cols=("actor_id", "first_name", "last_name"),
        filters=(_("first_name") == "Joe",)
    )) == """\
SELECT actor_id, first_name, last_name
FROM actor
WHERE (first_name = 'Joe')
"""


def test_query_2b():
    """ How to find all actors whose last name contain the letters `GEN` ? """
    assert str(Query(
        compact=False,
        table="actor",
        filters=(_("last_name") >> r"%GEN%",)
    )) == """\
SELECT *
FROM actor
WHERE (last_name LIKE '%GEN%')
"""


def test_query_2c():
    """ How to find all actors whose last names contain the letters `LI` and ordering the rows by last name and first name ? """
    assert str(Query(
        compact=False,
        table="actor",
        cols=(">:last_name", ">:first_name",),
        filters=(_("last_name") >> r"%LI%",),
    )) == """\
SELECT last_name, first_name
FROM actor
WHERE (last_name LIKE '%LI%')
ORDER BY last_name ASC, first_name ASC
"""


def test_query_2d():
    """ How to, using `IN`, display the `country_id` and `country` columns of the following countries Afghanistan, Bangladesh, and China ? """
    assert str(Query(
        compact=False,
        table="country",
        cols=("country_id", "country"),
        filters=(_("country") << ("Afghanistan", "Bangladesh", "China"),),
    )) == """\
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
    """ How to list the last names of actors, as well as how many actors have that last name ? """
    assert str(Query(
        compact=False,
        table="actor",
        cols=("last_name", count().alias("count")),
        groups=("last_name",),
    )) == """\
SELECT last_name, COUNT(*) AS count
FROM actor
GROUP BY last_name
"""


def test_query_4b():
    """ How to list last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors ? """
    assert str(Query(
        compact=False,
        table="actor",
        cols=("last_name", count().alias("count")),
        groups=("last_name",),
        filters=(count() > 1,),
    )) == """\
SELECT last_name, COUNT(*) AS count
FROM actor
GROUP BY last_name
HAVING (COUNT(*) > 1)
"""


def test_query_4c():
    """ Oh, no! The actor `HARPO WILLIAMS` was accidentally entered in the `actor` table as `GROUCHO WILLIAMS`, the name of Harpo"s second cousin"s husbands yoga teacher. Write a query to fix the record. """
    assert str(Query(
        compact=False,
        table="actor",
        query_mode=QueryMode.Update,
        assignations=((_("first_name") == "HARPO",)),
        filters=(((_("first_name") == "GROUCHO")) & (_("last_name") == "WILLIAMS"),)
    )) == """\
UPDATE actor
SET (first_name = 'HARPO')
WHERE ((first_name = 'GROUCHO') AND (last_name = 'WILLIAMS'))
"""


def test_query_4d():
    """ Perhaps we were too hasty in changing `GROUCHO` to `HARPO`. It turns out that `GROUCHO` was the correct name after all! In a
        single query, if the first name of the actor is currently `HARPO`, change it to `GROUCHO`. Otherwise, change the first name to
        `MUCHO GROUCHO`, as that is exactly what the actor will be with the grievous error. BE CAREFUL NOT TO CHANGE THE FIRST NAME OF
        EVERY ACTOR TO `MUCHO GROUCHO`, HOWEVER! (Hint: update the record using a unique identifier. """
    assert str(Query(
        compact=False,
        table="actor",
        query_mode=QueryMode.Update,
        assignations=(_("first_name") == When((_("first_name") == "HARPO",), ("GROUCHO",), "MUCHO GROUCHO"),),
        filters=((_("actor_id") == 172,))
    )) == """\
UPDATE actor
SET (first_name = CASE WHEN (first_name = 'HARPO') THEN 'GROUCHO' ELSE 'MUCHO GROUCHO' END)
WHERE (actor_id = 172)
"""


# 5a. You cannot locate the schema of the `address` table. Which query would you use to re-create it?

#   SHOW CREATE TABLE address;


def test_query_6a():
    """ How to, using `JOIN`, display the first and last names, as well as the address, of each staff member (use the tables `staff` and `address`) ? """
    assert str(Query(
        compact=False,
        table="staff",
        cols=("first_name", "last_name", "address"),
        joins=(("address", "address_id"),),
    )) == """\
SELECT first_name, last_name, address
FROM staff
INNER JOIN address
USING address_id
"""


def test_query_6b():
    """ How to, using `JOIN`, to display the total amount rung up by each staff member in August of 2005 (use tables `staff` and `payment`) ? """
    assert str(Query(
        compact=False,
        table="staff",
        cols=("first_name", "last_name", sum("amount")),
        joins=(("payment", "staff_id"),),
        filters=((month("payment_date") == 8) & (year("payment_date") == 2005),),
        groups=("staff_id",),
    )) == """\
SELECT first_name, last_name, SUM(amount)
FROM staff
INNER JOIN payment
USING staff_id
WHERE ((MONTH(payment_date) = 8) AND (YEAR(payment_date) = 2005))
GROUP BY staff_id
"""


def test_query_6c():
    """ How to list each film and the number of actors who are listed for that film (use tables `film_actor` and `film` and inner join) ? """
    assert str(Query(
        compact=False,
        table="film",
        cols=("title", count().alias("<:actor_count")),
        joins=(("film_actor", "film_id"),),
        groups=("title",),
    )) == """\
SELECT title, COUNT(*) AS actor_count
FROM film
INNER JOIN film_actor
USING film_id
GROUP BY title
ORDER BY actor_count DESC
"""


def test_query_6d():
    """ How many copies of the film `Hunchback Impossible` exist in the inventory system ? """
    assert str(Query(
        compact=False,
        table="film",
        cols=("title", count().alias("copies_count")),
        filters=(_("title") == "Hunchback Impossible",),
        joins=(("inventory", "film_id"),),
        groups=("title",)
    )) == """\
SELECT title, COUNT(*) AS copies_count
FROM film
INNER JOIN inventory
USING film_id
WHERE (title = 'Hunchback Impossible')
GROUP BY title
"""


def test_query_6e():
    """ How to, using the tables `payment` and `customer` and the `JOIN` command, list the total paid by each customer ? """
    assert str(Query(
        compact=False,
        table="customer",
        cols=(">:last_name", "first_name", sum("amount").alias("total_paid_amount")),
        joins=(("payment", "customer_id"),),
        groups=("last_name",)
    )) == """\
SELECT last_name, first_name, SUM(amount) AS total_paid_amount
FROM customer
INNER JOIN payment
USING customer_id
GROUP BY last_name
ORDER BY last_name ASC
"""


def test_query_7a():
    """ How to, using subqueries, display the titles of movies starting with the letters `K` and `Q` whose language is English ? """
    assert str(Query(
        compact=False,
        table="film",
        cols=("title",),
        filters=(
            ((_("title") >> "K%") | (_("title") >> "Q%")) & _("language_id") << Query(
                table="language",
                cols=("language_id",),
                filters=(_("name") == "English",),
            ),
        )
    )) == """\
SELECT title
FROM film
WHERE (((title LIKE 'K%') OR (title LIKE 'Q%')) AND (language_id IN (SELECT language_id FROM language WHERE (name = 'English'))))
"""


def test_query_7b():
    """ How to, using subqueries, display all actors who appear in the film `Alone Trip ? """
    assert str(Query(
        compact=False,
        table="actor",
        cols=("first_name", "last_name"),
        filters=(
            _("actor_id") << Query(
                table="film_actor",
                cols=("actor_id",),
                filters=(
                    _("film_id") << Query(
                        table="film",
                        cols=("film_id",),
                        filters=(_("title") == "Alone Trip",)
                    ),
                ),
            ),
        )
    )) == """\
SELECT first_name, last_name
FROM actor
WHERE (actor_id IN (SELECT actor_id FROM film_actor WHERE (film_id IN (SELECT film_id FROM film WHERE (title = 'Alone Trip')))))
"""


def test_query_7c():
    """ How to, knowing you want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers, retrieve this information (use joins) ? """
    assert str(Query(
        compact=False,
        cols=("first_name", "last_name", "email"),
        table="customer",
        joins=(("address", "address_id"), ("city", "city_id"), ("country", "country_id")),
        filters=(_("country") == "canada",)
    )) == """\
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
    """ How to identify all movies categorized as family films ? """
    assert str(Query(
        compact=False,
        table="film",
        cols=("title", "name"),
        joins=(("film_category", "film_id"), ("category", "category_id")),
        filters=(_("name") == "family",),
    )) == """\
SELECT title, name
FROM film
INNER JOIN film_category
USING film_id
INNER JOIN category
USING category_id
WHERE (name = 'family')
"""


def test_query_7e():
    """ How to display the most frequently rented movies in descending order ? """
    assert str(Query(
        compact=False,
        table="film",
        cols=("title", count().alias("<:rentals")),
        joins=(("inventory", "film_id"), ("rental", "inventory_id")),
        groups=("title",)
    )) == """\
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
    assert str(Query(
        compact=False,
        table="payment",
        cols=("store_id", sum("amount").alias("revenue")),
        joins=(("rental", "rental_id"), ("inventory", "inventory_id"), ("store", "store_id")),
        groups=("store_id",)
    )) == """\
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
    assert str(Query(
        compact=False,
        table="store",
        cols=("store_id", "city", "country"),
        joins=(("address", "address_id"), ("city", "city_id"), ("country", "country_id")),
    )) == """\
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
    """ List the top five genres in gross revenue in descending order (use the tables category, film_category, inventory, payment, and rental) ? """
    assert str(Query(
        compact=False,
        table="payment",
        cols=(sum("amount").alias("<:total_amount"), "name"),
        joins=(("rental", "rental_id"), ("inventory", "inventory_id"), ("category", "category_id")),
        groups=("name",)
    )) == """\
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


def test_query_8a():
    """ In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. Use the
        solution from the problem above to create a view. If you havent solved 7h, you can substitute another query to create a view. """
    assert str(View(
        name="top_five_genres",
        compact=False,
        query=Query(
            compact=False,
            table="payment",
            cols=(sum("amount").alias("<:total_sales"), "name:genre"),
            joins=(("rental", "rental_id"), ("inventory", "inventory_id"), ("film_category", "film_id"), ("category", "category_id")),
            groups=("name",),
            limit=5
        ))) == """\
CREATE VIEW top_five_genres AS
SELECT SUM(amount) AS total_sales, name AS genre
FROM payment
INNER JOIN rental
USING rental_id
INNER JOIN inventory
USING inventory_id
INNER JOIN film_category
USING film_id
INNER JOIN category
USING category_id
GROUP BY name
ORDER BY total_sales DESC
LIMIT 5
"""


def test_query_8b():
    """ How would you display the view that you created in 8a? """
    assert str(Query(
        compact=False,
        table="top_five_genres"
    )) == """\
SELECT *
FROM top_five_genres
"""


def test_query_8c():
    """ How would you display the view that you created in 8a? """
    assert str(View(
        name="top_five_genres",
        mode=ViewMode.Drop,
        compact=False,
    )) == """\
DROP VIEW top_five_genres
"""
