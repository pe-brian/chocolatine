from __future__ import annotations

from typing import Self

from typeguard import typechecked
from choc_expr import Expr as ChocExpr


@typechecked
class RawExpr(ChocExpr):
    """
    Raw SQL expression — wraps any SQL string verbatim.

    Use this as an escape hatch for expressions that Chocolatine
    doesn't support natively (e.g. NOW(), UUID(), custom functions).

    Examples:
        Col("updated_at") == RawExpr("NOW()")
        RawExpr("NOW()").alias("ts")
        RawExpr("CURRENT_USER()")
    """

    def __init__(self, sql: str, alias: str | None = None) -> None:
        self._sql = sql
        self._alias = alias
        super().__init__("{_sql}@{_alias}: AS {_alias}:;")

    @property
    def full_name(self) -> str:
        return self._sql

    def alias(self, name: str) -> Self:
        """ Set an alias """
        self._alias = name
        return self
