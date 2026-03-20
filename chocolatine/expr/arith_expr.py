from __future__ import annotations

from typing import Self

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from ..utils import quote_expr


@typechecked
class ArithExpr(ChocExpr):
    """
    Arithmetic expression — (left op right).

    Supports chaining: (Col("qty") * Col("price")) - Col("discount")
    Supports comparisons: (Col("qty") * Col("price")) > 100
    Supports alias for SELECT: (Col("qty") * Col("price")).alias("total")
    """

    def __init__(
            self,
            left: ChocExpr | int | float | str,
            op: str,
            right: ChocExpr | int | float | str,
            alias: str | None = None
    ) -> None:
        self._left = left
        self._op = op
        self._right = right
        self._alias = alias
        super().__init__("{full_name}@{_alias}: AS {_alias}:;")

    @staticmethod
    def _render(val: ChocExpr | int | float | str) -> str:
        if hasattr(val, "full_name"):
            return val.full_name
        return str(quote_expr(val))

    @property
    def full_name(self) -> str:
        return f"({self._render(self._left)} {self._op} {self._render(self._right)})"

    def alias(self, name: str) -> Self:
        """ Set an alias """
        self._alias = name
        return self

    # ── Arithmetic chaining ──────────────────────────────────────────────────

    def __add__(self, other: ChocExpr | int | float | str) -> ArithExpr:
        return ArithExpr(self, "+", other)

    def __radd__(self, other: ChocExpr | int | float | str) -> ArithExpr:
        return ArithExpr(other, "+", self)

    def __sub__(self, other: ChocExpr | int | float | str) -> ArithExpr:
        return ArithExpr(self, "-", other)

    def __rsub__(self, other: ChocExpr | int | float | str) -> ArithExpr:
        return ArithExpr(other, "-", self)

    def __mul__(self, other: ChocExpr | int | float | str) -> ArithExpr:
        return ArithExpr(self, "*", other)

    def __rmul__(self, other: ChocExpr | int | float | str) -> ArithExpr:
        return ArithExpr(other, "*", self)

    def __truediv__(self, other: ChocExpr | int | float | str) -> ArithExpr:
        return ArithExpr(self, "/", other)

    def __rtruediv__(self, other: ChocExpr | int | float | str) -> ArithExpr:
        return ArithExpr(other, "/", self)

    def __mod__(self, other: ChocExpr | int | float | str) -> ArithExpr:
        return ArithExpr(self, "%", other)

    # ── Comparisons (return Condition) ───────────────────────────────────────

    def __gt__(self, other):
        from .condition import Condition
        from ..enums.operator import Operator
        return Condition(self, Operator.GreaterThan, other)

    def __ge__(self, other):
        from .condition import Condition
        from ..enums.operator import Operator
        return Condition(self, Operator.GreaterOrEqualThan, other)

    def __lt__(self, other):
        from .condition import Condition
        from ..enums.operator import Operator
        return Condition(self, Operator.LowerThan, other)

    def __le__(self, other):
        from .condition import Condition
        from ..enums.operator import Operator
        return Condition(self, Operator.LowerOrEqualThan, other)

    def __eq__(self, other):
        from .condition import Condition
        from ..enums.operator import Operator
        return Condition(self, Operator.Equal, other)

    def __ne__(self, other):
        from .condition import Condition
        from ..enums.operator import Operator
        return Condition(self, Operator.NotEqual, other)
