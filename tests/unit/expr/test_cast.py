from chocolatine import Col as _, SqlType
from chocolatine.expr.cast import Cast


def test_cast_basic():
    assert Cast(_("price"), SqlType.Integer).build() == "CAST(price AS INT)"


def test_cast_with_alias():
    assert Cast(_("price"), SqlType.Integer, alias="int_price").build() == "CAST(price AS INT) AS int_price"


def test_cast_alias_method():
    assert Cast(_("price"), SqlType.Integer).alias("int_price").build() == "CAST(price AS INT) AS int_price"


def test_cast_string_type():
    assert Cast(_("code"), SqlType.String).build() == "CAST(code AS VARCHAR(255))"


def test_cast_literal():
    assert Cast(42, SqlType.String).build() == "CAST(42 AS VARCHAR(255))"
