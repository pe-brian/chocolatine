from chocolatine import quote_expr, str_to_bool


def test_quote_expr():
    assert quote_expr("donut") == "'donut'"
    assert quote_expr(1) == 1


def test_str_to_bool():
    assert str_to_bool("True") is True
    assert str_to_bool("False") is False
