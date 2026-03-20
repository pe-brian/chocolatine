from __future__ import annotations

from typing import Self

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from ..enums.sql_type import SqlType
from ..utils import quote_expr


@typechecked
class Cast(ChocExpr):
    """
    CAST expression — convert a value to the specified SQL type.

    Example:
        Cast(Col("price"), SqlType.Integer).alias("int_price")
        # CAST(price AS INT) AS int_price
    """

    def __init__(
            self,
            expr: ChocExpr | int | float | str,
            sql_type: SqlType,
            alias: str | None = None
    ) -> None:
        self._alias = alias
        self._source = expr.full_name if hasattr(expr, "full_name") else str(quote_expr(expr))
        self._sql_type = sql_type.value
        super().__init__("CAST({_source} AS {_sql_type})@{_alias}: AS {_alias}:;")

    def alias(self, name: str) -> Self:
        """ Set an alias """
        self._alias = name
        return self
