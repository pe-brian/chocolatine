from __future__ import annotations

from typing import TYPE_CHECKING

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

if TYPE_CHECKING:
    from .query import Query


@typechecked
class Subquery(ChocExpr):
    """
    Derived table — wraps a SELECT query for use in FROM or JOIN clauses.

    Example:
        sub = Subquery(Query.get_rows("orders", cols=[_("customer_id")]), alias="o")
        Query.get_rows(sub, cols=[_("o.customer_id")])
        # SELECT o.customer_id FROM (SELECT customer_id FROM orders) AS o
    """

    def __init__(self, query: Query, alias: str) -> None:
        self._subquery = query
        self._alias = alias
        super().__init__("({_subquery}) AS {_alias}")
