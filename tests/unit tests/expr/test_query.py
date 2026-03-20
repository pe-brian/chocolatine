from chocolatine import Query, QueryMode, Col as _, SqlType


def test_query_create_table():
    assert Query.create_table(
        table="people",
        cols=(
            _("first_name", type=SqlType.String),
            _("last_name", type=SqlType.String),
            _("age", type=SqlType.Integer),
            _("gender", type=SqlType.String),
            _("city", type=SqlType.String)
        )
    ).build() == "CREATE TABLE people (first_name VARCHAR(255), last_name VARCHAR(255), age INT, gender VARCHAR(255), city VARCHAR(255))"


def test_query_create_table_with_auto_id():
    assert Query.create_table(
        table="people",
        cols=(
            _("first_name", type=SqlType.String),
            _("last_name", type=SqlType.String),
            _("age", type=SqlType.Integer),
            _("gender", type=SqlType.String),
            _("city", type=SqlType.String)
        ),
        auto_id=True
    ).build() == "CREATE TABLE people (id MEDIUMINT NOT NULL AUTO_INCREMENT, first_name VARCHAR(255), last_name VARCHAR(255), age INT, gender VARCHAR(255), city VARCHAR(255), PRIMARY KEY (id))"


def test_query_alter_table_add_col():
    assert Query.add_col(
        table="people",
        col=_(name="country", type=SqlType.String)
    ).build() == "ALTER TABLE people ADD COLUMN country VARCHAR(255)"


def test_query_alter_table_add_col_after():
    assert Query.add_col(
        table="people",
        col=_(name="country", type=SqlType.String),
        after="city"
    ).build() == "ALTER TABLE people ADD COLUMN country VARCHAR(255) AFTER city"


def test_query_alter_table_rename_col():
    assert Query.rename_col(
        table="people",
        col="first_name",
        new_col="surname"
    ).build() == "ALTER TABLE people RENAME COLUMN first_name surname"


def test_query_alter_table_change_col():
    assert Query.change_col(
        table="people",
        col="name",
        new_col=_("age", type=SqlType.Integer)
    ).build() == "ALTER TABLE people CHANGE COLUMN name age INT"


def test_query_alter_table_drop_col():
    assert Query.drop_col(
        table="people",
        col="country"
    ).build() == "ALTER TABLE people DROP COLUMN country"


def test_query_insert_row_into_table():
    assert Query.insert_row(
        table="people",
        cols=(
            _("first_name", type=SqlType.String),
            _("last_name", type=SqlType.String),
            _("age", type=SqlType.Integer),
            _("gender", type=SqlType.String),
            _("city", type=SqlType.String)
        ),
        row=("jean", "mercier", 25, "M", "Toulouse")
    ).build() == "INSERT INTO people (first_name, last_name, age, gender, city) VALUES ('jean', 'mercier', 25, 'M', 'Toulouse')"


def test_query_insert_rows_into_table():
    assert Query.insert_rows(
        table="people",
        cols=(
            _("first_name", type=SqlType.String),
            _("last_name", type=SqlType.String),
            _("age", type=SqlType.Integer),
            _("gender", type=SqlType.String),
            _("city", type=SqlType.String)
        ),
        rows=(
            ("jean", "mercier", 25, "M", "Toulouse"),
            ("paul", "fabre", 18, "M", "Paris"),
            ("nathalie", "martin", 32, "F", "Bordeaux")
        )
    ).build() == "INSERT INTO people (first_name, last_name, age, gender, city) VALUES ('jean', 'mercier', 25, 'M', 'Toulouse'), ('paul', 'fabre', 18, 'M', 'Paris'), ('nathalie', 'martin', 32, 'F', 'Bordeaux')"


def test_query_update_rows():
    assert Query.update_rows(
        table="people",
        filters=(
            _("id") == 42,
        ),
        assignations=(
            _("name") == "bruno",
            _("age") == 52
        )
    ).build() == "UPDATE people SET (name = 'bruno'), (age = 52) WHERE (id = 42)"


def test_query_delete_rows_from_table():
    assert Query.delete_rows(
        table="people",
        filter=_("age") > 18
    ).build() == "DELETE FROM people WHERE (age > 18)"


def test_query_get_rows_from_table():
    assert Query.get_rows(
        table="people",
        filters=(_("age") > 18,)
    ).build() == "SELECT * FROM people WHERE (age > 18)"

def test_query_get_row_from_table():
    assert Query.get_row(
        table="people",
        filters=(_("age") > 18,)
    ).build() == "SELECT * FROM people WHERE (age > 18) LIMIT 1"


def test_query_delete_rows_no_filter():
    assert Query(query_mode=QueryMode.Delete, table="people").build() == "DELETE FROM people"


def test_query_delete_rows_multiple_filters():
    assert Query.delete_rows(
        table="people",
        filter=(_("age") > 18) & (_("city") == "Paris")
    ).build() == "DELETE FROM people WHERE ((age > 18) AND (city = 'Paris'))"


def test_query_get_rows_with_left_join():
    from chocolatine import JoinType
    assert Query.get_rows(
        table="people",
        joins=[("city", _("people.city_id") == _("city.id"), JoinType.Left)],
        cols=(_("first_name"), _("city.name"))
    ).build() == "SELECT first_name, city.name FROM people LEFT JOIN city ON (people.city_id = city.id)"


def test_query_get_rows_no_filter():
    assert Query.get_rows(table="people").build() == "SELECT * FROM people"


def test_query_read_mode():
    assert Query(query_mode=QueryMode.Select).read_mode is True
    assert Query(query_mode=QueryMode.Delete).read_mode is False


def test_query_update_mode():
    assert Query(query_mode=QueryMode.Update).update_mode is True
    assert Query(query_mode=QueryMode.Select).update_mode is False


def test_query_delete_mode():
    assert Query(query_mode=QueryMode.Delete).delete_mode is True
    assert Query(query_mode=QueryMode.Select).delete_mode is False


def test_query_fluent_table():
    q = Query(query_mode=QueryMode.Select)
    q.table("people")
    assert q.build() == "SELECT * FROM people"


def test_query_fluent_distinct():
    assert Query(query_mode=QueryMode.Select, table="people").distinct().build() == "SELECT DISTINCT(*) FROM people"


def test_query_fluent_head():
    q = Query(query_mode=QueryMode.Select, table="people")
    q.head(5)
    assert q.build() == "SELECT * FROM people LIMIT 5"


def test_query_rand():
    q1 = Query.get_rows(table="a")
    q2 = Query.get_rows(table="b")
    assert q2.__rand__(q1).build() == q2.union(q1).build()
