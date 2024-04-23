from chocolatine import GroupBy


def test_group_by_empty():
    assert GroupBy().build() == ""


def test_group_by():
    assert GroupBy(("a", "b", "c")).build() == "GROUP BY a, b, c"
