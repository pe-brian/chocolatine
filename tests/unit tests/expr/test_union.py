from chocolatine import Union, Query


def test_union():
    assert Union(Query(table="table_A"), Query(table="table_B"), compact=True).build() == "SELECT * FROM table_A UNION SELECT * FROM table_B"
    assert Union(Query(table="table_A", compact=False), Query(table="table_B", compact=False), compact=False).build() == "SELECT *\nFROM table_A\nUNION\nSELECT *\nFROM table_B\n"


def test_union_from_query():
    assert Query(table="table_A").union(Query(table="table_B")).build() == "SELECT * FROM table_A UNION SELECT * FROM table_B"
    assert Query(table="table_A", compact=False).union(Query(table="table_B", compact=False)).build() == "SELECT *\nFROM table_A\nUNION\nSELECT *\nFROM table_B\n"


def test_union_from_query_operator():
    assert (Query(table="table_A") & Query(table="table_B")).build() == "SELECT * FROM table_A UNION SELECT * FROM table_B"
    assert (Query(table="table_A", compact=False) & Query(table="table_B", compact=False)).build() == "SELECT *\nFROM table_A\nUNION\nSELECT *\nFROM table_B\n"
