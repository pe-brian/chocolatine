from chocolatine import Col as _
from chocolatine.expr.nullif import NullIf


def test_nullif_basic():
    assert NullIf(_("score"), 0).build() == "NULLIF(score, 0)"


def test_nullif_with_alias():
    assert NullIf(_("score"), 0, alias="s").build() == "NULLIF(score, 0) AS s"


def test_nullif_alias_method():
    assert NullIf(_("score"), 0).alias("s").build() == "NULLIF(score, 0) AS s"


def test_nullif_string_val():
    assert NullIf(_("status"), "deleted").build() == "NULLIF(status, 'deleted')"


def test_nullif_two_cols():
    assert NullIf(_("a"), _("b")).build() == "NULLIF(a, b)"
