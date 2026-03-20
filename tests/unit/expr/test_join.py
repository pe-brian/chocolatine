from chocolatine import Join, Table, Col as _, JoinType


def test_join_build_using_str_condition():
    assert Join(table=Table("table"), condition="a").build() == "INNER JOIN table USING a"


def test_join_build_using_str_condition_extended():
    assert Join(table=Table("table"), condition="a", compact=False).build() == "INNER JOIN table\nUSING a"


def test_join_build_using_iterable_str_condition():
    assert Join(table=Table("table"), condition=("a", "b", "c")).build() == "INNER JOIN table USING a, b, c"


def test_join_build_using_iterable_str_condition_extended():
    assert Join(table=Table("table"), condition=("a", "b", "c"), compact=False).build() == "INNER JOIN table\nUSING a, b, c"


def test_join_build_iterable_str_condition():
    assert Join(table=Table("table"), condition=_("a") > 1).build() == "INNER JOIN table ON (a > 1)"


def test_join_build_iterable_str_condition_extended():
    assert Join(table=Table("table"), condition=_("a") > 1, compact=False).build() == "INNER JOIN table\nON (a > 1)"


def test_join_left():
    assert Join(table=Table("table"), condition="a", join_type=JoinType.Left).build() == "LEFT JOIN table USING a"


def test_join_right():
    assert Join(table=Table("table"), condition="a", join_type=JoinType.Right).build() == "RIGHT JOIN table USING a"


def test_join_full():
    assert Join(table=Table("table"), condition="a", join_type=JoinType.Full).build() == "FULL JOIN table USING a"


def test_join_left_on_condition():
    assert Join(table=Table("table"), condition=_("a") == _("b"), join_type=JoinType.Left).build() == "LEFT JOIN table ON (a = b)"
