from chocolatine import ChocExpr


def test_choc_expr_empty():

    assert ChocExpr().build() == ""


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


def test_choc_expr_attr_should_not_be_evaluated():

    class Statement(ChocExpr):
        def __init__(self) -> None:
            self._a = "a"
            self.cond = False
            super().__init__("@{cond}:{a}:;")

        @property
        def a(self):
            raise ValueError()

    Statement().build()


def test_choc_expr_else_attr_should_not_be_evaluated():

    class Statement(ChocExpr):
        def __init__(self) -> None:
            self._a = "a"
            self.cond = True
            super().__init__("@{cond}::{a};")

        @property
        def a(self):
            raise ValueError()

    Statement().build()


def test_choc_expr_attr_with_endline():

    class NotBuildableSubExpr(ChocExpr):
        def __init__(self) -> None:
            super().__init__()

        @property
        def buildable(self):
            return False

    class Statement(ChocExpr):
        def __init__(self, expr):
            self.a = "a"
            self.b = "b"
            self.c = "c"
            self.d = NotBuildableSubExpr()
            super().__init__(choc_expr=expr, compact=False)

    assert Statement("{a~}").build() == "a\n"
    assert Statement("{a~}{b~}{c~}").build() == "a\nb\nc\n"


def test_choc_expr_with_not_buildable_attr_with_endline():

    class NotBuildableSubExpr(ChocExpr):
        def __init__(self) -> None:
            super().__init__()

        @property
        def buildable(self):
            return False

    class Statement(ChocExpr):
        def __init__(self, expr):
            self.a = "a"
            self.b = "b"
            self.c = "c"
            self.d = NotBuildableSubExpr()
            super().__init__(choc_expr=expr, compact=False)

    assert Statement("{a~}{b~}{d~}{c~}").build() == "a\nb\nc\n"


def test_choc_expr_with_endline_extended():

    class BuildableSubExpr(ChocExpr):
        def __init__(self, val) -> None:
            super().__init__(str(val))

    class Statement(ChocExpr):
        def __init__(self, expr):
            self.a = BuildableSubExpr("val_a")
            self.b = BuildableSubExpr("val_b")
            super().__init__(choc_expr=expr, compact=False)

    assert Statement("{a~}{b}").build() == "val_a\nval_b"
