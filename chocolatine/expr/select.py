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
        self.cols = cols
        self.unique = unique
        super().__init__("SELECT @{unique}:DISTINCT(:;@{empty}:*:{$cols};@{unique}:):;")

    @property
    def unique(self):
        return self._unique

    @unique.setter
    def unique(self, value):
        self._unique = value

    @property
    def empty(self):
        return len(self._cols) == 0

    @property
    def cols(self):
        return self._cols

    @cols.setter
    def cols(self, value):
        self._cols = [Col(col) if type(col) is str else col for col in (value or [])]
