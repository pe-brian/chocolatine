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
    trim,
    ltrim,
    rtrim,
    length,
    reverse,
    abs,
    round,
    floor,
    ceiling,
    date,
    md5,
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


def test_trim():
    assert str(trim("A")) == "TRIM(A)"


def test_ltrim():
    assert str(ltrim("A")) == "LTRIM(A)"


def test_rtrim():
    assert str(rtrim("A")) == "RTRIM(A)"


def test_length():
    assert str(length("A")) == "LENGTH(A)"


def test_reverse():
    assert str(reverse("A")) == "REVERSE(A)"


def test_abs():
    assert str(abs("A")) == "ABS(A)"


def test_round():
    assert str(round("A")) == "ROUND(A)"


def test_floor():
    assert str(floor("A")) == "FLOOR(A)"


def test_ceiling():
    assert str(ceiling("A")) == "CEILING(A)"


def test_date():
    assert str(date("A")) == "DATE(A)"


def test_md5():
    assert str(md5("A")) == "MD5(A)"
