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
