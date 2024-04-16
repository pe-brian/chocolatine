from chocolatine import ChocExpr


def test_choc_expr_without_interpolation():

    class Statement(ChocExpr):

        def __init__(self) -> None:
            self.values = (1, 2, 3)
            super().__init__("NOTHING")

    assert Statement().build() == "NOTHING"


def test_choc_expr_with_interpolation():

    class Statement(ChocExpr):

        def __init__(self) -> None:
            self.value = 1
            super().__init__("SOMETHING {value}")

    assert Statement().build() == "SOMETHING 1"


def test_choc_expr_loop():

    class Statement(ChocExpr):

        def __init__(self) -> None:
            self.values = (1, 2, 3)
            super().__init__("{$(values)}")

    assert Statement().build() == "1, 2, 3"


def test_choc_expr_loop_with_attribute():

    class Value:

        def __init__(self, value) -> None:
            self.value = value

    class Statement(ChocExpr):

        def __init__(self) -> None:
            self.values = (Value(1), Value(2), Value(3))
            super().__init__("{$(values).value}")

    assert Statement().build() == "1, 2, 3"
