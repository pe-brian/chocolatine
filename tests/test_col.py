from chocolatine import Col as _, AggFunction
from chocolatine.col import Col
from chocolatine.ordering import Ordering
from chocolatine.shortcut import lower


def test_col_init():
    col = _(name="amount", alias="new_amount", agg_function=AggFunction.Count, ordering=Ordering.Ascending)
    assert col._name == "amount"
    assert col._alias == "new_amount"
    assert col._agg_function == AggFunction.Count
    assert col._ordering == Ordering.Ascending


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
        ref="payment",
        agg_function=AggFunction.Sum
    )
    col.build()
    assert col._name == "amount"
    assert col._alias == "total_amount"
    assert col._ref == "payment"
    assert col._agg_function == AggFunction.Sum
    assert col._sql_function is None
    assert col._ordering is None
    assert col._concatenation == []


def test_col_alias():
    assert _("amount").alias("total_amount").build() != _("amount")
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
    assert col == "CONCAT(first_name, ' ', last_name)"
    assert col.alias("name").build() == "CONCAT(first_name, ' ', last_name) AS name"
    assert (Col("first_name") & " " & Col("last_name")).lower().build() == "LOWER(CONCAT(first_name, ' ', last_name))"
    assert (lower("first_name") & " " & lower("last_name")).build() == "CONCAT(LOWER(first_name), ' ', LOWER(last_name))"


def test_col_like():
    assert _("fruit").like("ap%").build() == "(fruit LIKE 'ap%')"
    assert (_("fruit") >> "ap%").build() == "(fruit LIKE 'ap%')"


def test_col_in():
    assert _("fruit").isin("banana", "apple", "strawberry").build() == "(fruit IN ('banana', 'apple', 'strawberry'))"
    assert (_("fruit") << ("banana", "apple", "strawberry")).build() == "(fruit IN ('banana', 'apple', 'strawberry'))"
