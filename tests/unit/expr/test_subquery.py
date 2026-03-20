from chocolatine import Query, Col as _
from chocolatine.expr.subquery import Subquery


def test_subquery_in_from():
    inner = Query.get_rows("orders", cols=[_("customer_id"), _("amount")])
    q = Query.get_rows(Subquery(inner, "o"), cols=[_("o.customer_id")])
    assert q.build() == "SELECT o.customer_id FROM (SELECT customer_id, amount FROM orders) AS o"


def test_subquery_in_join():
    base = Query.get_rows("orders")
    inner = Query.get_rows("order_items", cols=[_("order_id")])
    base.join(Subquery(inner, "oi"), _("oi.order_id") == _("orders.id"))
    assert "(SELECT order_id FROM order_items) AS oi" in base.build()


def test_subquery_renders_parentheses():
    inner = Query.get_rows("users", filters=[_("active") == 1])
    s = Subquery(inner, "u")
    assert s.build() == "(SELECT * FROM users WHERE (active = 1)) AS u"
