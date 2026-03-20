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


def test_condition_negate():
    from chocolatine import Col as _
    assert (~(_("age") > 25)).build() == "NOT (age > 25)"


def test_condition_chained_and():
    from chocolatine import Col as _
    assert ((_("age") > 18) & (_("age") < 65)).build() == "((age > 18) AND (age < 65))"


def test_condition_chained_or():
    from chocolatine import Col as _
    assert ((_("status") == "active") | (_("status") == "pending")).build() == "((status = 'active') OR (status = 'pending'))"
