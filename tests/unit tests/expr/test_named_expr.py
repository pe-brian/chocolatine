from chocolatine import NamedExpr


def test_named_expr_build():
    assert NamedExpr("ref.name").build() == "ref.name"
    assert NamedExpr("name").build() == "name"
    assert NamedExpr("name@alias").build() == "name AS alias"
    assert NamedExpr("ref.name@alias").build() == "ref.name AS alias"
