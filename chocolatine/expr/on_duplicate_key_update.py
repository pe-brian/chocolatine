from typing import Iterable

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from .condition import Condition


@typechecked
class OnDuplicateKeyUpdate(ChocExpr):
    """ ON DUPLICATE KEY UPDATE clause for INSERT statements """

    def __init__(
            self,
            assignations: Iterable[Condition] | None = None,
            compact: bool = True
    ) -> None:
        self.assignations = assignations or []
        super().__init__("ON DUPLICATE KEY UPDATE {$(assignations)}", compact=compact)

    @property
    def assignations(self):
        return self._assignations

    @assignations.setter
    def assignations(self, value: Iterable[Condition] | None):
        self._assignations = list(value or [])

    @property
    def buildable(self) -> bool:
        return len(self._assignations) > 0
