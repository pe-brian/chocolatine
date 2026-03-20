from chocolatine import Col as _


def test_replace():
    assert _("name").replace("foo", "bar").build() == "REPLACE(name, 'foo', 'bar')"


def test_replace_with_alias():
    assert _("name").replace("foo", "bar").alias("clean_name").build() == "REPLACE(name, 'foo', 'bar') AS clean_name"


def test_substring_with_length():
    assert _("description").substring(1, 100).build() == "SUBSTRING(description, 1, 100)"


def test_substring_without_length():
    assert _("description").substring(5).build() == "SUBSTRING(description, 5)"


def test_left():
    assert _("name").left(3).build() == "LEFT(name, 3)"


def test_right():
    assert _("name").right(3).build() == "RIGHT(name, 3)"


def test_lpad():
    assert _("code").lpad(10, "0").build() == "LPAD(code, 10, '0')"


def test_rpad():
    assert _("code").rpad(10, " ").build() == "RPAD(code, 10, ' ')"


def test_round_with_decimals():
    assert _("score").round(2).build() == "ROUND(score, 2)"


def test_round_without_decimals():
    assert _("score").round().build() == "ROUND(score)"


def test_date_format():
    assert _("created_at").date_format("%Y-%m").build() == "DATE_FORMAT(created_at, '%Y-%m')"


def test_date_format_full():
    assert _("created_at").date_format("%Y-%m-%d %H:%i:%s").build() == "DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s')"


def test_table_prefixed_col_with_multiarg():
    assert _("u.first_name").replace("foo", "bar").build() == "REPLACE(u.first_name, 'foo', 'bar')"


def test_multiarg_function_resets_on_new_call():
    col = _("score").round(2)
    col.round()
    assert col.build() == "ROUND(score)"
