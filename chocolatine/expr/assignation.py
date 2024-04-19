from .col import Col
from .choc_expr import ChocExpr


class Assignation(ChocExpr):
    """ Assignation expression """
    def __init__(self, col: Col | str, val: Col | str | int | float) -> None:
        self._col = col if isinstance(col, Col) else Col(col)
        if isinstance(val, Col):
            val = val.full_name
        self._val = val
        super().__init__("{_col.full_name} = " + f"{self._val}")
