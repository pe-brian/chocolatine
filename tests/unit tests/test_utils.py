from chocolatine import quote_expr, to_bool


def test_quote_expr():
    assert quote_expr("donut") == "'donut'"
    assert quote_expr(1) == 1


def test_to_bool():
    assert to_bool("True") is True
    assert to_bool("Hello") is True
    assert to_bool(1) is True
    assert to_bool("False") is False
    assert to_bool(None) is False
    assert to_bool("None") is False
    assert to_bool(0) is False
