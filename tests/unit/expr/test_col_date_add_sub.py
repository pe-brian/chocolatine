from chocolatine import Col as _, IntervalUnit


def test_date_add_days():
    assert _("created_at").date_add(7, IntervalUnit.Day).build() == "DATE_ADD(created_at, INTERVAL 7 DAY)"


def test_date_add_months():
    assert _("created_at").date_add(1, IntervalUnit.Month).build() == "DATE_ADD(created_at, INTERVAL 1 MONTH)"


def test_date_add_with_alias():
    assert _("created_at").date_add(7, IntervalUnit.Day).alias("expires_at").build() == "DATE_ADD(created_at, INTERVAL 7 DAY) AS expires_at"


def test_date_sub_days():
    assert _("event_date").date_sub(30, IntervalUnit.Day).build() == "DATE_SUB(event_date, INTERVAL 30 DAY)"


def test_date_sub_years():
    assert _("birth_date").date_sub(18, IntervalUnit.Year).build() == "DATE_SUB(birth_date, INTERVAL 18 YEAR)"
