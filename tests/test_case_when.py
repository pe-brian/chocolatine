from chocolatine import ConditionalCaseWhen, CaseWhen, Col as _


def test_case_when():
    assert CaseWhen(_("a"), (1, 2, 3), ("un", "deux", "trois"), "autre").build() == """\
CASE a
WHEN 1 THEN 'un'
WHEN 2 THEN 'deux'
WHEN 3 THEN 'trois'
ELSE 'autre'
END\
"""


def test_conditional_case_when():
    assert ConditionalCaseWhen((_("a") == 1, _("a") == 2, _("a") == 3), ("un", "deux", "trois"), "autre").build() == """\
CASE
WHEN (a = 1) THEN 'un'
WHEN (a = 2) THEN 'deux'
WHEN (a = 3) THEN 'trois'
ELSE 'autre'
END\
""" 
