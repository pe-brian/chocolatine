from chocolatine import UpdateSet, Table, Col as _


def test_update_set_empty():
    assert UpdateSet().build() == ""


def test_update_set_build():
    assert UpdateSet(
        table=Table("table"),
        assignations=(_("col_A") == 1, _("col_B") == 2)
    ).build() == "UPDATE table SET (col_A = 1), (col_B = 2)"
    assert UpdateSet(
        table=Table("table"),
        assignations=(_("col_A") == _("col_C"), _("col_B") == _("col_D"))
    ).build() == "UPDATE table SET (col_A = col_C), (col_B = col_D)"


def test_update_set_build_extended():
    assert UpdateSet(
        table=Table("table"),
        assignations=(_("col_A") == 1, _("col_B") == 2),
        compact=False
    ).build() == "UPDATE table\nSET (col_A = 1), (col_B = 2)"
    assert UpdateSet(
        table=Table("table"),
        assignations=(_("col_A") == _("col_C"), _("col_B") == _("col_D")),
        compact=False
    ).build() == "UPDATE table\nSET (col_A = col_C), (col_B = col_D)"
