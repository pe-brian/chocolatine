from chocolatine import Col as _, AggFunction, Ordering, lower


def test_col_init():
    col = _(name="amount", alias="new_amount", agg_function=AggFunction.Count, ordering=Ordering.Ascending)
    assert col._name == "amount"
    assert col._alias == "new_amount"
    assert col._agg_function == AggFunction.Count
    assert col._ordering == Ordering.Ascending


def test_col_init_with_name():
    assert _("table.name@alias").build() == "table.name AS alias"
    assert _("table.name:alias").build() == "table.name AS alias"


def test_col_build():
    assert _("amount").build() == "amount"
    assert _("amount").build() == str(_("amount"))
    assert _("amount", agg_function=AggFunction.Sum).build() == "SUM(amount)"
    assert _("amount", "total_amount", AggFunction.Sum).build() == "SUM(amount) AS total_amount"
    assert _("amount", "total_amount").build() == "amount AS total_amount"


def test_col_build_immutable():
    col = _(
        name="amount",
        alias="total_amount",
        table_name="payment",
        agg_function=AggFunction.Sum
    )
    col.build()
    assert col._name == "amount"
    assert col._alias == "total_amount"
    assert col._table_name == "payment"
    assert col._agg_function == AggFunction.Sum
    assert col._sql_function is None
    assert col._ordering is None
    assert col._concatenation == []


def test_col_alias():
    assert _("amount").alias("total_amount") != _("amount")
    assert _("amount").alias("total_amount").build() == "amount AS total_amount"


def test_col_sum():
    assert _("amount").sum().build() == "SUM(amount)"
    assert _("amount").sum().build() == _("amount", agg_function=AggFunction.Sum).build()


def test_col_count():
    assert _("amount").count().build() == "COUNT(amount)"
    assert _("amount").count().build() == _("amount", agg_function=AggFunction.Count).build()


def test_col_max():
    assert _("amount").max().build() == "MAX(amount)"
    assert _("amount").max().build() == _("amount", agg_function=AggFunction.Max).build()


def test_col_min():
    assert _("amount").min().build() == "MIN(amount)"
    assert _("amount").min().build() == _("amount", agg_function=AggFunction.Min).build()


def test_col_average():
    assert _("amount").average().build() == "AVG(amount)"
    assert _("amount").average().build() == _("amount", agg_function=AggFunction.Average).build()


def test_col_concat():
    col = _("first_name") & " " & _("last_name")
    assert type(col) is _
    assert col.build() == "CONCAT(first_name, ' ', last_name)"
    assert col.alias("name").build() == "CONCAT(first_name, ' ', last_name) AS name"
    assert (_("first_name") & " " & _("last_name")).lower().build() == "LOWER(CONCAT(first_name, ' ', last_name))"
    assert (lower("first_name") & " " & lower("last_name")).build() == "CONCAT(LOWER(first_name), ' ', LOWER(last_name))"


def test_col_like():
    assert _("fruit").like("ap%").build() == "(fruit LIKE 'ap%')"
    assert (_("fruit") >> "ap%").build() == "(fruit LIKE 'ap%')"


def test_col_in():
    assert _("fruit").isin(("banana", "apple", "strawberry")).build() == "(fruit IN ('banana', 'apple', 'strawberry'))"
    assert (_("fruit") << ("banana", "apple", "strawberry")).build() == "(fruit IN ('banana', 'apple', 'strawberry'))"


def test_col_greater_than():
    assert (_("age") > 25).build() == "(age > 25)"


def test_col_greater_or_equal_than():
    assert (_("age") >= 25).build() == "(age >= 25)"
    

def test_col_lower_than():
    assert (_("age") < 25).build() == "(age < 25)"


def test_col_lower_or_equal_than():
    assert (_("age") <= 25).build() == "(age <= 25)"


def test_col_invalid_name_empty():
    import pytest
    with pytest.raises(ValueError):
        _("")


def test_col_invalid_name_chars():
    import pytest
    with pytest.raises(ValueError):
        _("invalid; DROP TABLE users--")


def test_col_star_with_alias_raises():
    import pytest
    with pytest.raises(ValueError):
        _("*", alias="a")


def test_col_star_with_table_name_raises():
    import pytest
    with pytest.raises(ValueError):
        _("*", table_name="t")


def test_col_ordering_prefix_asc():
    assert _(">:amount").build() == "amount"
    assert _(">:amount")._ordering.value == "ASC"


def test_col_ordering_prefix_desc():
    assert _("<:amount").build() == "amount"
    assert _("<:amount")._ordering.value == "DESC"


def test_col_star_with_ordering_raises():
    import pytest
    from chocolatine import Ordering
    with pytest.raises(ValueError):
        _("*", ordering=Ordering.Ascending)


def test_col_rand():
    col = "prefix" & _("name")
    assert col.build() == "CONCAT(name, 'prefix')"


def test_col_order():
    from chocolatine import Ordering
    assert _("amount").order(Ordering.Descending)._ordering == Ordering.Descending


def test_col_asc():
    from chocolatine import Ordering
    assert _("amount").asc()._ordering == Ordering.Ascending


def test_col_desc():
    from chocolatine import Ordering
    assert _("amount").desc()._ordering == Ordering.Descending


def test_col_alias_with_asc_prefix():
    from chocolatine import Ordering
    col = _("amount").alias(">:total")
    assert col._alias == "total"
    assert col._ordering == Ordering.Ascending


def test_col_alias_with_desc_prefix():
    from chocolatine import Ordering
    col = _("amount").alias("<:total")
    assert col._alias == "total"
    assert col._ordering == Ordering.Descending


def test_col_aggregate():
    from chocolatine import AggFunction
    assert _("amount").aggregate(AggFunction.Sum).build() == "SUM(amount)"
    assert _("amount").aggregate(AggFunction.Average).build() == "AVG(amount)"


def test_col_trim():
    assert _("name").trim().build() == "TRIM(name)"


def test_col_ltrim():
    assert _("name").ltrim().build() == "LTRIM(name)"


def test_col_rtrim():
    assert _("name").rtrim().build() == "RTRIM(name)"


def test_col_length():
    assert _("name").length().build() == "LENGTH(name)"


def test_col_reverse():
    assert _("name").reverse().build() == "REVERSE(name)"


def test_col_abs():
    assert _("score").abs().build() == "ABS(score)"


def test_col_round():
    assert _("score").round().build() == "ROUND(score)"


def test_col_floor():
    assert _("score").floor().build() == "FLOOR(score)"


def test_col_ceiling():
    assert _("score").ceiling().build() == "CEILING(score)"


def test_col_date():
    assert _("created_at").date().build() == "DATE(created_at)"


def test_col_md5():
    assert _("password").md5().build() == "MD5(password)"


def test_col_count_distinct():
    assert _("customer_id").count_distinct().build() == "COUNT(DISTINCT customer_id)"


def test_col_creation_name_not_null():
    from chocolatine import SqlType
    assert _("email", type=SqlType.String, not_null=True).creation_name == "email VARCHAR(255) NOT NULL"


def test_col_creation_name_unique():
    from chocolatine import SqlType
    assert _("email", type=SqlType.String, unique=True).creation_name == "email VARCHAR(255) UNIQUE"


def test_col_creation_name_default_int():
    from chocolatine import SqlType
    assert _("score", type=SqlType.Integer, default=0).creation_name == "score INT DEFAULT 0"


def test_col_creation_name_default_str():
    from chocolatine import SqlType
    assert _("status", type=SqlType.String, default="active").creation_name == "status VARCHAR(255) DEFAULT 'active'"


def test_col_creation_name_all_constraints():
    from chocolatine import SqlType
    assert _("email", type=SqlType.String, not_null=True, unique=True).creation_name == "email VARCHAR(255) NOT NULL UNIQUE"


def test_col_set_not_null_fluent():
    from chocolatine import SqlType
    col = _("email", type=SqlType.String).set_not_null()
    assert col._not_null is True
    assert col.creation_name == "email VARCHAR(255) NOT NULL"


def test_col_set_unique_fluent():
    from chocolatine import SqlType
    col = _("email", type=SqlType.String).set_unique()
    assert col._unique is True
    assert col.creation_name == "email VARCHAR(255) UNIQUE"


def test_col_set_default_fluent():
    from chocolatine import SqlType
    col = _("score", type=SqlType.Integer).set_default(0)
    assert col._default == 0
    assert col.creation_name == "score INT DEFAULT 0"

