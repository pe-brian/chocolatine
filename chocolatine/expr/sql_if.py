from __future__ import annotations

from typing import Self

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from ..utils import quote_expr


@typechecked
class SqlIf(ChocExpr):
    """
    MySQL IF() function — evaluates a condition and returns one of two values.

    Example:
        SqlIf(Col("score") >= 50, "pass", "fail").alias("result")
        # IF((score >= 50), 'pass', 'fail') AS result
    """

    def __init__(
            self,
            condition: ChocExpr,
            true_val: ChocExpr | int | float | str,
            false_val: ChocExpr | int | float | str,
            alias: str | None = None
    ) -> None:
        self._alias = alias
        self._condition = condition.build()
        self._true = true_val.full_name if hasattr(true_val, "full_name") else str(quote_expr(true_val))
        self._false = false_val.full_name if hasattr(false_val, "full_name") else str(quote_expr(false_val))
        super().__init__("IF({_condition}, {_true}, {_false})@{_alias}: AS {_alias}:;")

    def alias(self, name: str) -> Self:
        """ Set an alias """
        self._alias = name
        return self
