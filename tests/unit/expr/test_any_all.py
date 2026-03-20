from chocolatine import Query, Col as _
from chocolatine.expr.any_all import AnySubquery, AllSubquery


def test_any_greater_than():
    sub = Query.get_rows("products", cols=[_("price")])
    cond = _("price") > AnySubquery(sub)
    assert cond.build() == "(price > ANY (SELECT price FROM products))"


def test_any_equal():
    sub = Query.get_rows("categories", cols=[_("id")])
    cond = _("category_id") == AnySubquery(sub)
    assert cond.build() == "(category_id = ANY (SELECT id FROM categories))"


def test_all_less_than():
    sub = Query.get_rows("prices", cols=[_("amount")])
    cond = _("budget") < AllSubquery(sub)
    assert cond.build() == "(budget < ALL (SELECT amount FROM prices))"


def test_all_in_filter():
    sub = Query.get_rows("products", cols=[_("price")])
    q = Query.get_rows("orders", filters=[_("total") > AllSubquery(sub)])
    assert "ALL (SELECT price FROM products)" in q.build()
