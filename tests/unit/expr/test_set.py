from chocolatine import Set, Col as _


def test_set_empty():
    assert Set().build() == ""


def test_set_build():
    assert Set((_('col') == 1,)).build() == 'SET (col = 1)'
