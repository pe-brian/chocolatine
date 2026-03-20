import pytest
from chocolatine import With, Query, Col as _


def _active_users():
    return Query.get_rows("users", filters=[_("active") == 1])


def _big_orders():
    return Query.get_rows("orders", filters=[_("amount") > 100])


def test_with_single_cte():
    q = With(ctes=[("active_users", _active_users())], query=Query.get_rows("active_users"))
    assert q.build() == "WITH active_users AS (SELECT * FROM users WHERE (active = 1)) SELECT * FROM active_users"


def test_with_multiple_ctes():
    q = With(
        ctes=[("active_users", _active_users()), ("big_orders", _big_orders())],
        query=Query.get_rows("active_users")
    )
    assert q.build() == (
        "WITH active_users AS (SELECT * FROM users WHERE (active = 1)), "
        "big_orders AS (SELECT * FROM orders WHERE (amount > 100)) "
        "SELECT * FROM active_users"
    )


def test_with_non_compact():
    q = With(ctes=[("active_users", _active_users())], query=Query.get_rows("active_users"), compact=False)
    assert q.build() == (
        "WITH\n"
        "active_users AS (\n"
        "SELECT * FROM users WHERE (active = 1)\n"
        ")\n"
        "SELECT * FROM active_users"
    )


def test_with_recursive():
    base = Query.get_rows("employees", filters=[_("manager_id").is_null()])
    rec = Query.get_rows("employees")
    recursive_q = base.union_all(rec)
    q = With(ctes=[("org", recursive_q)], query=Query.get_rows("org"), recursive=True)
    assert q.build().startswith("WITH RECURSIVE org AS (")


def test_with_main_query_has_cols_and_filters():
    q = With(
        ctes=[("active_users", _active_users())],
        query=Query.get_rows("active_users", cols=[_("id"), _("name")], filters=[_("age") > 18])
    )
    assert q.build() == (
        "WITH active_users AS (SELECT * FROM users WHERE (active = 1)) "
        "SELECT id, name FROM active_users WHERE (age > 18)"
    )


def test_with_empty_ctes_raises():
    with pytest.raises(ValueError):
        With(ctes=[], query=Query.get_rows("users"))
