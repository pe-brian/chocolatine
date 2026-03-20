from __future__ import annotations

from typing import Self

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from ..utils import quote_expr


@typechecked
class NullIf(ChocExpr):
    """
    NULLIF expression — returns NULL if both arguments are equal, otherwise the first argument.

    Example:
        NullIf(Col("score"), 0).alias("score")
        # NULLIF(score, 0) AS score
    """

    def __init__(
            self,
            expr: ChocExpr | int | float | str,
            null_val: ChocExpr | int | float | str,
            alias: str | None = None
    ) -> None:
        self._alias = alias
        self._left = expr.full_name if hasattr(expr, "full_name") else str(quote_expr(expr))
        self._right = null_val.full_name if hasattr(null_val, "full_name") else str(quote_expr(null_val))
        super().__init__("NULLIF({_left}, {_right})@{_alias}: AS {_alias}:;")

    def alias(self, name: str) -> Self:
        """ Set an alias """
        self._alias = name
        return self
