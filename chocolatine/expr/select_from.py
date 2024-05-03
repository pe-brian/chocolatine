from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from .table import Table
    from .col import Col

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from .from_expr import FromExpr
from .select import Select


@typechecked
class SelectFrom(ChocExpr):
    """ Select expression """
    def __init__(
            self,
            table: str | Table | None = None,
            cols: Iterable[str | Col] | None = None,
            unique: bool = False,
            compact: bool = True
    ) -> None:
        self._select = Select(cols=cols, unique=unique, compact=compact)
        self._from_expr = FromExpr(table=table, compact=compact)
        super().__init__("{select~}{from_expr}", compact=compact)

    @property
    def select(self):
        return self._select

    @property
    def from_expr(self):
        return self._from_expr

    @property
    def buildable(self) -> bool:
        return self._from_expr.buildable
