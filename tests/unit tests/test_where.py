from chocolatine import Where, Col as _


def test_where_empty():
    assert Where().build() == ""


def test_where():
    assert Where((_("a") > _("b")) & (_("c") > 2)).build() == "WHERE ((a > b) AND (c > 2))"
