from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .table import Table

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from .from_expr import FromExpr
from .delete import Delete


@typechecked
class DeleteFrom(ChocExpr):
    """ Delete expression """
    def __init__(
            self,
            table: str | Table | None = None,
            compact: bool = True
    ) -> None:
        self._delete = Delete(compact=compact)
        self._from_expr = FromExpr(table=table, compact=compact)
        super().__init__("{delete~}{from_expr}", compact=compact)

    @property
    def delete(self):
        return self._delete

    @property
    def from_expr(self):
        return self._from_expr

    @property
    def buildable(self) -> bool:
        return self._from_expr.buildable
