from chocolatine import SelectFrom


def test_select_from_no_args():
    assert SelectFrom().build() == ""
    assert SelectFrom(cols=("a", "b", "c")).build() == ""


def test_select_from_build():
    assert SelectFrom(table="table").build() == """\
SELECT *
FROM table\
"""
    assert SelectFrom(table="table", cols=("a", "b", "c")).build() == """\
SELECT a, b, c
FROM table\
"""
    assert SelectFrom(table="table", cols=("a", "b", "c"), unique=True).build() == """\
SELECT DISTINCT(a, b, c)
FROM table\
"""
    assert SelectFrom(table="table", unique=True).build() == """\
SELECT DISTINCT(*)
FROM table\
"""


def test_select_from_update():
    sf = SelectFrom(table="table")
    sf.select.cols = ["a", "b", "c"]
    assert sf.build() == """\
SELECT a, b, c
FROM table\
"""
