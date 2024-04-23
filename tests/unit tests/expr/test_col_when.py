from chocolatine import ColWhen, Col as _


def test_when_without_else():
    assert str(ColWhen(_("a"), (1, 2, 3), ("un", "deux", "trois"))) == """\
CASE a
WHEN 1 THEN 'un'
WHEN 2 THEN 'deux'
WHEN 3 THEN 'trois'
END\
"""


def test_when_without_else_compact():
    assert str(ColWhen(_("a"), (1, 2, 3), ("un", "deux", "trois"), compact=True)) == "CASE a WHEN 1 THEN 'un' WHEN 2 THEN 'deux' WHEN 3 THEN 'trois' END"


def test_when_with_else():
    assert str(ColWhen(_("a"), (1, 2, 3), ("un", "deux", "trois"), "autre")) == """\
CASE a
WHEN 1 THEN 'un'
WHEN 2 THEN 'deux'
WHEN 3 THEN 'trois'
ELSE 'autre'
END\
"""


def test_when_with_else_compact():
    assert str(ColWhen(_("a"), (1, 2, 3), ("un", "deux", "trois"), "autre", compact=True)) == "CASE a WHEN 1 THEN 'un' WHEN 2 THEN 'deux' WHEN 3 THEN 'trois' ELSE 'autre' END"
