from __future__ import annotations

from typing import Self

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from ..utils import quote_expr


@typechecked
class IfNull(ChocExpr):
    """
    IFNULL expression — returns the second argument if the first is NULL.

    Example:
        IfNull(Col("phone"), "N/A").alias("contact")
        # IFNULL(phone, 'N/A') AS contact
    """

    def __init__(
            self,
            expr: ChocExpr | int | float | str,
            fallback: ChocExpr | int | float | str,
            alias: str | None = None
    ) -> None:
        self._alias = alias
        self._left = expr.full_name if hasattr(expr, "full_name") else str(quote_expr(expr))
        self._right = fallback.full_name if hasattr(fallback, "full_name") else str(quote_expr(fallback))
        super().__init__("IFNULL({_left}, {_right})@{_alias}: AS {_alias}:;")

    def alias(self, name: str) -> Self:
        """ Set an alias """
        self._alias = name
        return self
