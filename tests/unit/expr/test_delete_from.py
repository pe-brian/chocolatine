from chocolatine import DeleteFrom


def test_delete_from_no_args():
    assert DeleteFrom().build() == ""


def test_delete_from_build():
    assert DeleteFrom(table="table").build() == "DELETE FROM table"


def test_delete_from_build_extended():
    assert DeleteFrom(table="table", compact=False).build() == "DELETE\nFROM table"
