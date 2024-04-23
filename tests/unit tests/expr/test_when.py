from chocolatine import When, Col as _


def test_conditional_when_with_else():
    assert str(When((_("a") == 1, _("a") == 2, _("a") == 3), ("un", "deux", "trois"), "autre")) == """\
CASE
WHEN (a = 1) THEN 'un'
WHEN (a = 2) THEN 'deux'
WHEN (a = 3) THEN 'trois'
ELSE 'autre'
END\
"""


def test_conditional_when_with_else_compact():
    assert str(When((_("a") == 1, _("a") == 2, _("a") == 3), ("un", "deux", "trois"), "autre", compact=True)) == "CASE WHEN (a = 1) THEN 'un' WHEN (a = 2) THEN 'deux' WHEN (a = 3) THEN 'trois' ELSE 'autre' END"


def test_conditional_when_without_else():
    assert str(When((_("a") == 1, _("a") == 2, _("a") == 3), ("un", "deux", "trois"))) == """\
CASE
WHEN (a = 1) THEN 'un'
WHEN (a = 2) THEN 'deux'
WHEN (a = 3) THEN 'trois'
END\
"""


def test_conditional_when_without_else_compact():
    assert str(When((_("a") == 1, _("a") == 2, _("a") == 3), ("un", "deux", "trois"), compact=True)) == "CASE WHEN (a = 1) THEN 'un' WHEN (a = 2) THEN 'deux' WHEN (a = 3) THEN 'trois' END"
