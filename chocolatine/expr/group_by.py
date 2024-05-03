from typing import Iterable

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from .col import Col


@typechecked
class GroupBy(ChocExpr):
    """ GroupBy expression """
    def __init__(
            self,
            cols: Iterable[Col | str] | None = None,
            compact: bool = True
    ) -> None:
        self.cols = cols
        super().__init__("GROUP BY {$(cols)}", compact=compact)

    @property
    def cols(self):
        return self._cols

    @cols.setter
    def cols(self, value: Iterable[Col | str] | None):
        if value is not None and len(value) < 1:
            raise ValueError("The number of cols must be at least 1")
        self._cols = [Col(col) if type(col) is str else col for col in (value or [])]

    @property
    def buildable(self):
        return self.cols is not None and len(self.cols) > 0
