import pytest

from chocolatine import (
    concat,
    count,
    sum,
    asc,
    desc,
    upper,
    lower,
    second,
    minute,
    hour,
    day,
    month,
    year,
    Col as _
)


def test_concat():
    with pytest.raises(ValueError):
        concat()
    with pytest.raises(ValueError):
        concat(_("A"))
    assert str(concat(_("A"), _("B"), _("C"))) == "CONCAT(A, B, C)"


def test_count():
    assert str(count()) == "COUNT(*)"
    assert str(count(col_name="A")) == "COUNT(A)"


def test_sum():
    assert str(sum("A")) == "SUM(A)"


def test_upper():
    assert str(upper("A")) == "UPPER(A)"


def test_lower():
    assert str(lower("A")) == "LOWER(A)"


def test_second():
    assert str(second("A")) == "SECOND(A)"


def test_minute():
    assert str(minute("A")) == "MINUTE(A)"


def test_hour():
    assert str(hour("A")) == "HOUR(A)"


def test_day():
    assert str(day("A")) == "DAY(A)"


def test_month():
    assert str(month("A")) == "MONTH(A)"


def test_year():
    assert str(year("A")) == "YEAR(A)"


def test_asc():
    assert asc("A").ordering_label == "A ASC"


def test_desc():
    assert desc("A").ordering_label == "A DESC"
