from chocolatine import Query


def test_intersect():
    q1 = Query.get_rows("a")
    q2 = Query.get_rows("b")
    assert q1.intersect(q2).build() == "SELECT * FROM a INTERSECT SELECT * FROM b"


def test_intersect_all():
    q1 = Query.get_rows("a")
    q2 = Query.get_rows("b")
    assert q1.intersect_all(q2).build() == "SELECT * FROM a INTERSECT ALL SELECT * FROM b"


def test_except():
    q1 = Query.get_rows("a")
    q2 = Query.get_rows("b")
    assert q1.except_(q2).build() == "SELECT * FROM a EXCEPT SELECT * FROM b"


def test_except_all():
    q1 = Query.get_rows("a")
    q2 = Query.get_rows("b")
    assert q1.except_all(q2).build() == "SELECT * FROM a EXCEPT ALL SELECT * FROM b"
