from chocolatine import ConditionalCaseWhen, CaseWhen, Col as _


def test_case_when_without_else():
    assert CaseWhen(_("a"), (1, 2, 3), ("un", "deux", "trois")))) == """\
CASE a
WHEN 1 THEN 'un'
WHEN 2 THEN 'deux'
WHEN 3 THEN 'trois'
END\
"""


def test_case_when_with_else():
    assert CaseWhen(_("a"), (1, 2, 3), ("un", "deux", "trois"), "autre"))) == """\
CASE a
WHEN 1 THEN 'un'
WHEN 2 THEN 'deux'
WHEN 3 THEN 'trois'
ELSE 'autre'
END\
"""


def test_conditional_case_when_with_else():
    assert ConditionalCaseWhen((_("a") == 1, _("a") == 2, _("a") == 3), ("un", "deux", "trois"), "autre"))) == """\
CASE
WHEN (a = 1) THEN 'un'
WHEN (a = 2) THEN 'deux'
WHEN (a = 3) THEN 'trois'
ELSE 'autre'
END\
"""


def test_conditional_case_when_without_else():
    assert ConditionalCaseWhen((_("a") == 1, _("a") == 2, _("a") == 3), ("un", "deux", "trois")))) == """\
CASE
WHEN (a = 1) THEN 'un'
WHEN (a = 2) THEN 'deux'
WHEN (a = 3) THEN 'trois'
END\
"""
