from chocolatine import Update, Table


def test_update_empty():
    assert Update().build() == ""


def test_build():
    assert Update("table").build() == "UPDATE table"
    assert Update(Table("table")).build() == "UPDATE table"
