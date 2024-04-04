from chocolatine import Col, Condition, Operator, AggFunction
from chocolatine.ordering import Ordering


def test_condition_op_eq():
    assert Condition("res", Operator.Equal, 42).build() == "('res' = 42)"


def test_condition_op_ne():
    assert Condition("res", Operator.NotEqual, 42).build() == "('res' <> 42)"


def test_condition_op_gt():
    assert Condition("res", Operator.GreaterThan, 42).build() == "('res' > 42)"


def test_condition_op_ge():
    assert Condition("res", Operator.GreaterOrEqualThan, 42).build() == "('res' >= 42)"


def test_condition_op_lt():
    assert Condition("res", Operator.LowerThan, 42).build() == "('res' < 42)"


def test_condition_op_le():
    assert Condition("res", Operator.LowerOrEqualThan, 42).build() == "('res' <= 42)"


def test_condition_op_and():
    assert Condition(42, Operator.And, 42).build() == "(42 AND 42)"


def test_condition_op_or():
    assert Condition(42, Operator.Or, 42).build() == "(42 OR 42)"


def test_condition_op_like():
    assert Condition(42, Operator.Like, 42).build() == "(42 LIKE 42)"


###

def test_col_init():
    col = Col(name="amount", new_name="new_amount", agg_function=AggFunction.Count, ordering=Ordering.Ascending)
    assert col._name == "amount"
    assert col._new_name == "new_amount"
    assert col._agg_function == AggFunction.Count
    assert col._ordering == Ordering.Ascending


def test_col_build():
    assert Col("amount").build() == "'amount'"
    assert Col("amount").build() == str(Col("amount"))
    assert Col("amount", agg_function=AggFunction.Sum).build() == "SUM('amount')"
    assert Col("amount", "total_amount", AggFunction.Sum).build() == "SUM('amount') AS 'total_amount'"
    assert Col("amount", "total_amount").build() == "'amount' AS 'total_amount'"


def test_col_build_immutable():
    col = Col(
        name="amount",
        new_name="total_amount",
        ref_table="payment",
        agg_function=AggFunction.Sum
    )
    col.build()
    assert col._name == "amount"
    assert col._new_name == "total_amount"
    assert col._ref_table == "payment"
    assert col._agg_function == AggFunction.Sum
    assert col._sql_function is None
    assert col._ordering is None
    assert col._concatenation == []


def test_col_alias():
    assert Col("amount").alias("total_amount").build() != Col("amount")
    assert Col("amount").alias("total_amount").build() == "'amount' AS 'total_amount'"


def test_col_summ():
    assert Col("amount").sum().build() == "SUM('amount')"
    assert Col("amount").sum().build() == Col("amount", agg_function=AggFunction.Sum).build()


def test_col_count():
    assert Col("amount").count().build() == "COUNT('amount')"
    assert Col("amount").count().build() == Col("amount", agg_function=AggFunction.Count).build()


def test_col_max():
    assert Col("amount").max().build() == "MAX('amount')"
    assert Col("amount").max().build() == Col("amount", agg_function=AggFunction.Max).build()


def test_col_min():
    assert Col("amount").min().build() == "MIN('amount')"
    assert Col("amount").min().build() == Col("amount", agg_function=AggFunction.Min).build()


def test_col_average():
    assert Col("amount").average().build() == "AVG('amount')"
    assert Col("amount").average().build() == Col("amount", agg_function=AggFunction.Average).build()


def test_col_concat():
    col = Col("first_name") & " " & Col("last_name")
    assert type(col) is Col
    assert col == "CONCAT('first_name', ' ', 'last_name')"
    assert col.alias("name").build() == "CONCAT('first_name', ' ', 'last_name') AS 'name'"
