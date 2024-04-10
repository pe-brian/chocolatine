from chocolatine.expr import Expr


def test_expr():
    assert Expr(name="name", alias="alias", ref="table").build() == "table.name AS alias"
    assert Expr(name="table.name@alias").build() == "table.name AS alias"
    assert Expr(name="table.name:alias").build() == "table.name AS alias"
