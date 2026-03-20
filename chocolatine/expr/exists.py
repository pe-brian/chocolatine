from __future__ import annotations

from typing import Self, TYPE_CHECKING

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

if TYPE_CHECKING:
    from .query import Query


@typechecked
class Exists(ChocExpr):
    """ EXISTS / NOT EXISTS subquery expression """

    def __init__(self, query: Query, negate: bool = False) -> None:
        """
        Build an EXISTS (subquery) expression.

        :param query: The subquery to test for existence.
        :param negate: If True, produce NOT EXISTS instead.
        """
        self._query = query
        self._negate = negate
        super().__init__("@{_negate}:NOT :;EXISTS ({_query})")

    def __invert__(self) -> Self:
        return Exists(self._query, negate=not self._negate)
