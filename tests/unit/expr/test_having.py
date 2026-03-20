from chocolatine import Having, Col as _


def test_having_no_args():
    assert Having().build() == ""


def test_having():
    assert Having((_("a") > _("b")) & (_("c") > 2)).build() == "HAVING ((a > b) AND (c > 2))"
