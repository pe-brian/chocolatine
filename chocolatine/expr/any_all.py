from __future__ import annotations

from typing import TYPE_CHECKING

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

if TYPE_CHECKING:
    from .query import Query


@typechecked
class AnySubquery(ChocExpr):
    """
    ANY subquery — use with comparison operators to match any row in the subquery.

    Example:
        Col("price") > AnySubquery(Query.get_rows("products", cols=[_("price")]))
        # (price > ANY (SELECT price FROM products))
    """

    def __init__(self, query: Query) -> None:
        self._query = query
        super().__init__("ANY ({_query})")


@typechecked
class AllSubquery(ChocExpr):
    """
    ALL subquery — use with comparison operators to match all rows in the subquery.

    Example:
        Col("price") > AllSubquery(Query.get_rows("products", cols=[_("price")]))
        # (price > ALL (SELECT price FROM products))
    """

    def __init__(self, query: Query) -> None:
        self._query = query
        super().__init__("ALL ({_query})")
