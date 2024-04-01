from chocolatine import Col, Condition, Operator, AggFunction
from chocolatine.ordering import Ordering


def test_condition_op_eq():
    assert Condition(42, Operator.Equal, 42).build() == "(42 = 42)"


def test_condition_op_ne():
    assert Condition(42, Operator.NotEqual, 42).build() == "(42 <> 42)"


def test_condition_op_gt():
    assert Condition(42, Operator.GreaterThan, 42).build() == "(42 > 42)"


def test_condition_op_ge():
    assert Condition(42, Operator.GreaterOrEqualThan, 42).build() == "(42 >= 42)"


def test_condition_op_lt():
    assert Condition(42, Operator.LowerThan, 42).build() == "(42 < 42)"


def test_condition_op_le():
    assert Condition(42, Operator.LowerOrEqualThan, 42).build() == "(42 <= 42)"


def test_condition_op_and():
    assert Condition(42, Operator.And, 42).build() == "(42 AND 42)"


def test_condition_op_or():
    assert Condition(42, Operator.Or, 42).build() == "(42 OR 42)"


def test_condition_op_like():
    assert Condition(42, Operator.Like, 42).build() == "(42 LIKE 42)"


###

def test_col_init():
    col = Col(name="amount", new_name="new_amount", agg_function=AggFunction.Count, ordering=Ordering.Ascending)
    assert col.name == "amount"
    assert col.new_name == "new_amount"
    assert col.agg_function == AggFunction.Count
    assert col.ordering == Ordering.Ascending


def test_col_build():
    assert Col("amount").build() == "amount"
    assert Col("amount").build() == str(Col("amount"))
    assert Col("amount", agg_function=AggFunction.Sum).build() == "SUM(amount)"
    assert Col("amount", "total_amount", AggFunction.Sum).build() == "SUM(amount) AS total_amount"
    assert Col("amount", "total_amount").build() == "amount AS total_amount"


def test_col_build_immutable():
    col = Col(
        name="amount",
        new_name="total_amount",
        ref_table="payment",
        agg_function=AggFunction.Sum
    )
    col.build()
    assert col.name == "amount"
    assert col.new_name == "total_amount"
    assert col.ref_table == "payment"
    assert col.agg_function == AggFunction.Sum
    assert col.sql_function is None
    assert col.ordering is None
    assert col.concatenation == []


def test_col_alias():
    assert Col("amount").alias("total_amount") != Col("amount")
    assert Col("amount").alias("total_amount") == "amount AS total_amount"


def test_col_sum():
    assert Col("amount").sum() == "SUM(amount)"
    assert Col("amount").sum() == Col("amount", agg_function=AggFunction.Sum).build()


def test_col_count():
    assert Col("amount").count() == "COUNT(amount)"
    assert Col("amount").count() == Col("amount", agg_function=AggFunction.Count).build()


def test_col_max():
    assert Col("amount").max() == "MAX(amount)"
    assert Col("amount").max() == Col("amount", agg_function=AggFunction.Max).build()


def test_col_min():
    assert Col("amount").min() == "MIN(amount)"
    assert Col("amount").min() == Col("amount", agg_function=AggFunction.Min).build()


def test_col_average():
    assert Col("amount").average() == "AVG(amount)"
    assert Col("amount").average() == Col("amount", agg_function=AggFunction.Average).build()


def test_col_concat():
    assert Col(Col("first_name") & " " & Col("last_name")).alias("name").build() == "CONCAT(first_name, ' ', last_name) AS name"
