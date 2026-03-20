from __future__ import annotations

from typing import Self

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from .col import Col
from ..utils import quote_expr


@typechecked
class Coalesce(ChocExpr):
    """ COALESCE expression — returns the first non-NULL value from the given arguments """

    def __init__(
            self,
            *args: Col | str | int | float | None,
            alias: str | None = None
    ) -> None:
        """
        Build a COALESCE(arg1, arg2, ...) expression.

        :param args: Two or more columns or literal values.
        :param alias: Optional alias (AS clause).
        """
        if len(args) < 2:
            raise ValueError("COALESCE requires at least 2 arguments")
        self._alias = alias
        self._args = [a.full_name if isinstance(a, Col) else ("NULL" if a is None else str(quote_expr(a))) for a in args]
        super().__init__("COALESCE({$(_args)})@{_alias}: AS {_alias}:;")

    def alias(self, name: str) -> Self:
        """ Set an alias """
        self._alias = name
        return self
