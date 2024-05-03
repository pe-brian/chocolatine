from __future__ import annotations
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .col import Col
    from .when import When

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from ..utils import quote_expr
from ..operator import Operator


@typechecked
class Condition(ChocExpr):
    """ SQL condition """
    def __init__(
            self,
            left_value: int | float | str | Col | Self,
            op: Operator,
            right_value: int | float | str | Col | When | Self,
            negate: bool = False
    ) -> None:
        self._left_value = left_value
        self._op = op
        self._right_value = right_value
        self._negate = negate

        super().__init__("@{negate}:NOT :;({left_val} {op} {right_val})")

    @property
    def negate(self):
        return self._negate

    @property
    def op(self):
        return self._op.value

    @property
    def left_val(self):
        return quote_expr(self._left_value)

    @property
    def right_val(self):
        try:
            return f"({self._right_value.build()})" if self._op == Operator.In else self._right_value.build()
        except AttributeError:
            pass
        return quote_expr(self._right_value)

    def __and__(self, other: int | float | str | Col | Self) -> Self:
        return Condition(left_value=self, op=Operator.And, right_value=other)

    def __rand__(self, other: int | float | str | Col | Self) -> Self:
        return self.__and__(other)

    def __or__(self, other: int | float | str | Col | Self) -> Self:
        return Condition(left_value=self, op=Operator.Or, right_value=other)

    def __ror__(self, other: int | float | str | Col | Self) -> Self:
        return self.__or__(other)

    def __invert__(self) -> Self:
        return Condition(left_value=self._left_value, op=self._op, right_value=self._right_value, negate=True)
