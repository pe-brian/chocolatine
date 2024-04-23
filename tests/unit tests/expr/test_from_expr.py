from chocolatine import FromExpr, Table


def test_from_expr_empty():
    assert FromExpr().build() == ""


def test_from_expr_without_ref_and_without_alias():
    assert FromExpr("table").build() == "FROM table"
    assert FromExpr(Table("table")).build() == "FROM table"


def test_from_expr_with_ref_and_without_alias():
    assert FromExpr("schema.table").build() == "FROM schema.table"
    assert FromExpr(Table("schema.table")).build() == "FROM schema.table"


def test_from_expr_without_ref_and_with_alias():
    assert FromExpr("table@tb").build() == "FROM table AS tb"
    assert FromExpr(Table("table@tb")).build() == "FROM table AS tb"


def test_from_expr_with_ref_and_alias():
    assert FromExpr("schema.table@tb").build() == "FROM schema.table AS tb"
    assert FromExpr(Table("schema.table@tb")).build() == "FROM schema.table AS tb"
