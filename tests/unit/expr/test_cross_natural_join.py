from chocolatine import Query, JoinType


def test_cross_join():
    q = Query.get_rows("a")
    q.join("b", join_type=JoinType.Cross)
    assert q.build() == "SELECT * FROM a CROSS JOIN b"


def test_natural_join():
    q = Query.get_rows("a")
    q.join("b", join_type=JoinType.Natural)
    assert q.build() == "SELECT * FROM a NATURAL JOIN b"


def test_cross_join_in_constructor():
    q = Query.get_rows("a", joins=[("b", None, JoinType.Cross)])
    assert q.build() == "SELECT * FROM a CROSS JOIN b"
