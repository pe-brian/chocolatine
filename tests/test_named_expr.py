from chocolatine import NamedExpr


def test_named_expr_build():
    assert NamedExpr(name="name", alias="alias", ref="table").build() == "table.name AS alias"
    assert NamedExpr(name="table.name@alias").build() == "table.name AS alias"
    assert NamedExpr(name="table.name:alias").build() == "table.name AS alias"
