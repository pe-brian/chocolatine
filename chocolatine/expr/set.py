from typing import Iterable
from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from .col import Col
from .condition import Condition


@typechecked
class Set(ChocExpr):
    """ Set expression """
    def __init__(
            self,
            assignations: Iterable[Condition] | None = None,
            compact: bool = True
    ) -> None:
        self.assignations = assignations or []
        super().__init__("SET {$(assignations)}", compact=compact)

    @property
    def assignations(self):
        return self._cols

    @assignations.setter
    def assignations(self, value):
        self._cols = [Col(col) if type(col) is str else col for col in (value or [])]

    @property
    def buildable(self):
        return len(self.assignations) > 0
