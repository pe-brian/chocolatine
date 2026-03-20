from chocolatine import OrderBy, Col as _, Select


def test_order_by_not_buildable():
    assert OrderBy(Select((_("a"), _("b"), _("c")))).build() == ""


def test_order_by():
    assert OrderBy(Select((_(">:a"), _("b"), _("<:c")))).build() == "ORDER BY a ASC, c DESC"
