from chocolatine import Select, Table


def test_select_empty():
    assert Select().build() == "SELECT *"


def test_select():
    assert Select(cols=("ref.TableA:a", "ref.TableB:b")).build() == "SELECT ref.TableA AS a, ref.TableB AS b"
    assert Select(cols=(Table("ref.TableA:a"), Table("ref.TableB:b"))).build() == "SELECT ref.TableA AS a, ref.TableB AS b"


def test_select_distinct():
    assert Select(cols=("ref.TableA:a", "ref.TableB:b"), unique=True).build() == "SELECT DISTINCT(ref.TableA AS a, ref.TableB AS b)"
    assert Select(cols=(Table("ref.TableA:a"), Table("ref.TableB:b")), unique=True).build() == "SELECT DISTINCT(ref.TableA AS a, ref.TableB AS b)"
