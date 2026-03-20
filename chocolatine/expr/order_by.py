from typing import Iterable

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from .select import Select
from .col import Col
from ..enums.ordering import Ordering


@typechecked
class OrderBy(ChocExpr):
    """ OrderBy expression """
    def __init__(
            self,
            select: Select,
            compact: bool = True
    ) -> None:
        self._select = select
        self._explicit_cols: list = []
        super().__init__("ORDER BY {$(cols).ordering_label}", compact=compact)

    def set_explicit(self, *cols: Col | str) -> None:
        processed = []
        for col in cols:
            if isinstance(col, str):
                col = Col(col)
            if col._ordering is None:
                col._ordering = Ordering.Ascending
            processed.append(col)
        self._explicit_cols = processed

    @property
    def cols(self) -> Iterable[Col]:
        if self._explicit_cols:
            return self._explicit_cols
        return [col for col in self._select.cols if isinstance(col, Col) and col.ordering_label]

    @property
    def buildable(self) -> bool:
        return len(self.cols) > 0
