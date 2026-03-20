from chocolatine import Col as _


def test_datediff_two_cols():
    assert _("end_date").datediff(_("start_date")).build() == "DATEDIFF(end_date, start_date)"


def test_datediff_col_and_string():
    assert _("end_date").datediff("2024-01-01").build() == "DATEDIFF(end_date, '2024-01-01')"


def test_datediff_with_alias():
    assert _("end_date").datediff(_("start_date")).alias("days").build() == "DATEDIFF(end_date, start_date) AS days"
