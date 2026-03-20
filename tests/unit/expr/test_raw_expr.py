from chocolatine import Col as _, Query
from chocolatine.expr.raw_expr import RawExpr


def test_raw_expr_build():
    assert RawExpr("NOW()").build() == "NOW()"


def test_raw_expr_with_alias():
    assert RawExpr("NOW()", alias="ts").build() == "NOW() AS ts"


def test_raw_expr_alias_method():
    assert RawExpr("NOW()").alias("ts").build() == "NOW() AS ts"


def test_raw_expr_full_name():
    assert RawExpr("CURRENT_USER()").full_name == "CURRENT_USER()"


def test_raw_expr_in_condition():
    cond = _("updated_at") == RawExpr("NOW()")
    assert cond.build() == "(updated_at = NOW())"


def test_raw_expr_in_select():
    q = Query.get_rows("users", cols=[RawExpr("NOW()").alias("ts")])
    assert "NOW() AS ts" in q.build()


def test_raw_expr_where_routing():
    # RawExpr without agg function should go to WHERE, not HAVING
    q = Query.get_rows("t")
    q.filter(_("x") == RawExpr("NOW()"))
    built = q.build()
    assert "WHERE" in built
    assert "HAVING" not in built
