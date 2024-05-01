from chocolatine import View, Query, ViewMode


def test_view_creation():
    assert View(name="View", query=Query(table="Table")).build() == "CREATE VIEW View AS SELECT * FROM Table"
    assert View(name="View", query=Query(table="Table"), compact=False).build() == "CREATE VIEW View AS\nSELECT * FROM Table"


def test_view_dropping():
    assert View(name="View", mode=ViewMode.Drop).build() == "DROP VIEW View"
    assert View(name="View", mode=ViewMode.Drop, compact=False).build() == "DROP VIEW View\n"
