import pytest

from chocolatine import Where, Col as _


def test_where():
    with pytest.raises(ValueError):
        Where().build()
    assert Where((_("a") > _("b")) & (_("c") > 2)).build() == "WHERE ((a > b) AND (c > 2))"
