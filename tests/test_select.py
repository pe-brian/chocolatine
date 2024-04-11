from chocolatine import Select, Table


def test_select_empty():
    assert Select().build() == "SELECT *"


def test_select():
    assert Select(("ref.TableA:a", "ref.TableB:b")).build() == "SELECT ref.TableA AS a, ref.TableB AS b"
    assert Select((Table("ref.TableA:a"), Table("ref.TableB:b"))).build() == "SELECT ref.TableA AS a, ref.TableB AS b"
