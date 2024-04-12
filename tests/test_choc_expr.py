from chocolatine import ChocExpr


def test_choc_expr_build():

    class Statement(ChocExpr):

        def __init__(self) -> None:
            self.values = (1, 2, 3)
            super().__init__("{$values}")

    assert Statement().build() == "1, 2, 3"
