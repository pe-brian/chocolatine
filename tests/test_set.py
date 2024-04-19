from chocolatine import Set, Assignation, Col


def test_set_empty():
    assert Set().build() == ""


def test_set_build():
    assert Set((Assignation(Col('col'), 1),)).build() == 'SET col = 1'
