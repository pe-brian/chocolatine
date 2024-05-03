from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from .table import Table
    from .condition import Condition

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from .update import Update
from .set import Set


@typechecked
class UpdateSet(ChocExpr):
    """ UpdateSet expression """
    def __init__(
            self,
            table: str | Table | None = None,
            assignations: Iterable[Condition] | None = None,
            compact: bool = True
    ) -> None:
        self._update = Update(table=table, compact=compact)
        self._set = Set(assignations=assignations, compact=compact)
        super().__init__("{_update~}{_set}", compact=compact)

    @property
    def buildable(self) -> bool:
        return self._update.buildable and self._set.buildable
