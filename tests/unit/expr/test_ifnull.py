from chocolatine import Col as _
from chocolatine.expr.ifnull import IfNull


def test_ifnull_basic():
    assert IfNull(_("phone"), "N/A").build() == "IFNULL(phone, 'N/A')"


def test_ifnull_with_alias():
    assert IfNull(_("phone"), "N/A").alias("contact").build() == "IFNULL(phone, 'N/A') AS contact"


def test_ifnull_two_cols():
    assert IfNull(_("phone"), _("mobile")).build() == "IFNULL(phone, mobile)"


def test_ifnull_numeric_fallback():
    assert IfNull(_("score"), 0).build() == "IFNULL(score, 0)"
