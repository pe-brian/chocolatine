from typing import Iterable
from typeguard import typechecked

from .col import Col
from .choc_expr import ChocExpr


@typechecked
class Select(ChocExpr):
    """ Select expression """
    def __init__(
            self,
            cols: Iterable[Col | str] | None = None,
            unique: bool = False
    ) -> None:
        self._cols = [Col(col) if type(col) is str else col for col in (cols or [])]
        self._unique = unique
        super().__init__(
            choc_expr="SELECT @{unique}:DISTINCT(:;@{empty}:*:{joigned_cols};@{unique}:):;",
            unique=self.unique,
            empty=self.empty,
            joigned_cols=", ".join(str(col) for col in self._cols)
        )

    @property
    def unique(self):
        return self._unique

    @property
    def empty(self):
        return len(self._cols) == 0
