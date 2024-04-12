import pytest

from chocolatine import Having, Col as _


def test_having():
    with pytest.raises(ValueError):
        Having().build()
    assert Having((_("a") > _("b")) & (_("c") > 2)).build() == "HAVING ((a > b) AND (c > 2))"
