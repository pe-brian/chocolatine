from chocolatine import Query, QueryMode, Col as _, SqlType


def test_query_create_table():
    assert Query(
        query_mode=QueryMode.Create,
        table="people",
        cols=(
            _("first_name", type=SqlType.String),
            _("last_name", type=SqlType.String),
            _("age", type=SqlType.Integer),
            _("gender", type=SqlType.String),
            _("city", type=SqlType.String)
        )
    ).build() == "CREATE TABLE people (first_name VARCHAR(255), last_name VARCHAR(255), age INT, gender VARCHAR(255), city VARCHAR(255))"
