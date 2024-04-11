from chocolatine import NamedExpr


def test_expr():
    assert NamedExpr(name="name", alias="alias", ref="table").build() == "table.name AS alias"
    assert NamedExpr(name="table.name@alias").build() == "table.name AS alias"
    assert NamedExpr(name="table.name:alias").build() == "table.name AS alias"
