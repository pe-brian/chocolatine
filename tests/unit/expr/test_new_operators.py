import pytest
from chocolatine import Col as _, Condition, Operator, SqlType, Limit, Query


# IS NULL / IS NOT NULL

def test_col_is_null():
    assert _("email").is_null().build() == "(email IS NULL)"


def test_col_is_not_null():
    assert _("email").is_not_null().build() == "(email IS NOT NULL)"


def test_col_is_null_negated():
    assert (~_("email").is_null()).build() == "NOT (email IS NULL)"


def test_condition_is_null():
    assert Condition(_("email"), Operator.IsNull).build() == "(email IS NULL)"


def test_condition_is_not_null():
    assert Condition(_("email"), Operator.IsNotNull).build() == "(email IS NOT NULL)"


# BETWEEN

def test_col_between_ints():
    assert _("age").between(18, 65).build() == "(age BETWEEN 18 AND 65)"


def test_col_between_strings():
    assert _("name").between("a", "m").build() == "(name BETWEEN 'a' AND 'm')"


def test_col_between_negated():
    assert (~_("age").between(18, 65)).build() == "NOT (age BETWEEN 18 AND 65)"


def test_condition_between():
    assert Condition(_("age"), Operator.Between, 18, between_high=65).build() == "(age BETWEEN 18 AND 65)"


# LIMIT + OFFSET

def test_limit_with_offset():
    assert Limit(length=10, offset=20).build() == "LIMIT 10 OFFSET 20"


def test_limit_without_offset():
    assert Limit(length=10).build() == "LIMIT 10"


def test_limit_offset_zero_raises():
    with pytest.raises(ValueError):
        Limit(length=10, offset=-1)


def test_query_with_limit_and_offset():
    assert Query.get_rows(table="people", limit=10, offset=20).build() == "SELECT * FROM people LIMIT 10 OFFSET 20"


def test_query_fluent_offset():
    q = Query.get_rows(table="people")
    q.head(10).offset(20)
    assert q.build() == "SELECT * FROM people LIMIT 10 OFFSET 20"


# SQL Types

def test_sql_type_values():
    assert SqlType.Integer.value == "INT"
    assert SqlType.BigInteger.value == "BIGINT"
    assert SqlType.Text.value == "TEXT"
    assert SqlType.Date.value == "DATE"
    assert SqlType.DateTime.value == "DATETIME"
    assert SqlType.Timestamp.value == "TIMESTAMP"
    assert SqlType.Json.value == "JSON"
    assert SqlType.Decimal.value == "DECIMAL"
    assert SqlType.Blob.value == "BLOB"


def test_col_creation_name_new_types():
    assert _("created_at", type=SqlType.DateTime).creation_name == "created_at DATETIME"
    assert _("data", type=SqlType.Json).creation_name == "data JSON"
    assert _("score", type=SqlType.BigInteger).creation_name == "score BIGINT"
