from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from .table import Table
    from .col import Col

from typeguard import typechecked

from .from_expr import FromExpr
from .select import Select

from .choc_expr import ChocExpr


@typechecked
class SelectFrom(ChocExpr):
    """ Select expression """
    def __init__(
            self,
            table: str | Table | None = None,
            cols: Iterable[str | Col] | None = None,
            unique: bool = False
    ) -> None:
        self._select = Select(cols=cols, unique=unique)
        self._from_expr = FromExpr(table=table)
        super().__init__("{select}\n{from_expr}")

    @property
    def select(self):
        return self._select

    @property
    def from_expr(self):
        return self._from_expr
