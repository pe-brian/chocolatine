from chocolatine import Exists, Query, Col as _


def test_exists():
    subq = Query.get_rows("orders", filters=[_("user_id") == _("users.id")])
    assert Exists(subq).build() == "EXISTS (SELECT * FROM orders WHERE (user_id = users.id))"


def test_not_exists_param():
    subq = Query.get_rows("orders", filters=[_("user_id") == _("users.id")])
    assert Exists(subq, negate=True).build() == "NOT EXISTS (SELECT * FROM orders WHERE (user_id = users.id))"


def test_not_exists_invert():
    subq = Query.get_rows("orders", filters=[_("user_id") == _("users.id")])
    assert (~Exists(subq)).build() == "NOT EXISTS (SELECT * FROM orders WHERE (user_id = users.id))"


def test_exists_double_invert():
    subq = Query.get_rows("orders")
    assert (~~Exists(subq)).build() == "EXISTS (SELECT * FROM orders)"


def test_exists_as_filter():
    subq = Query.get_rows("orders", filters=[_("user_id") == _("users.id")])
    q = Query.get_rows("users").filter(Exists(subq))
    assert q.build() == "SELECT * FROM users WHERE EXISTS (SELECT * FROM orders WHERE (user_id = users.id))"


def test_not_exists_as_filter():
    subq = Query.get_rows("orders", filters=[_("user_id") == _("users.id")])
    q = Query.get_rows("users").filter(~Exists(subq))
    assert q.build() == "SELECT * FROM users WHERE NOT EXISTS (SELECT * FROM orders WHERE (user_id = users.id))"


def test_exists_with_cols():
    subq = Query.get_rows("orders", cols=[_("id")], filters=[_("user_id") == _("users.id")])
    assert Exists(subq).build() == "EXISTS (SELECT id FROM orders WHERE (user_id = users.id))"
