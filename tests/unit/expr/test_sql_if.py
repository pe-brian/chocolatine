from chocolatine import Col as _
from chocolatine.expr.sql_if import SqlIf


def test_sql_if_basic():
    assert SqlIf(_("score") >= 50, "pass", "fail").build() == "IF((score >= 50), 'pass', 'fail')"


def test_sql_if_with_alias():
    assert SqlIf(_("score") >= 50, "pass", "fail").alias("result").build() == "IF((score >= 50), 'pass', 'fail') AS result"


def test_sql_if_numeric_values():
    assert SqlIf(_("active") == 1, 1, 0).build() == "IF((active = 1), 1, 0)"


def test_sql_if_col_values():
    assert SqlIf(_("a") > _("b"), _("a"), _("b")).build() == "IF((a > b), a, b)"
