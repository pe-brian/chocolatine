from chocolatine import Request, Col, Condition, Operator, AggFunction


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


def test_col_build():
    assert Col("amount").build() == "amount"
    assert Col("amount", agg_function=AggFunction.Sum).build() == "sum(amount)"
    assert Col("amount", "total_amount", AggFunction.Sum).build() == "sum(amount) AS total_amount"
    assert Col("amount").sum() == "sum(amount)"
    assert Col("amount").sum().alias("total_amount") == "sum(amount) AS total_amount"


def test_request_001():
    assert Request(compact=True) \
        .table("payment") \
        .select(Col("staff_id").asc(), Col("amount").alias("total_amount").sum().desc()) \
        .group_by("staff_id") \
        .filter((Col("amount") > 0.99) & ~(Col("customer_id") == 3)) \
        .build() == \
        "SELECT staff_id, sum(amount) AS total_amount FROM payment WHERE ((amount > 0.99) AND NOT(customer_id = 3)) GROUP BY staff_id ORDER BY staff_id ASC, amount DESC"
