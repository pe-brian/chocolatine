from chocolatine import Condition, Operator


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


def test_condition_op_in():
    assert Condition(42, Operator.In, (1, 2, 24, 42)).build() == "(42 IN (1, 2, 24, 42))"
