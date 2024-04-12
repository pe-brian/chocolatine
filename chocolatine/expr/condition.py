from __future__ import annotations
from typing import Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .col import Col

from typeguard import typechecked

from ..utils import quote_expr
from . import ChocExpr
from ..operator import Operator


@typechecked
class Condition(ChocExpr):
    """ SQL condition """
    def __init__(
            self,
            left_value: int | float | str | Col | Self,
            op: Operator,
            right_value: int | float | str | Col | Self,
            negate: bool = False
    ) -> None:
        self._left_value = left_value
        self._op = op
        self._right_value = right_value
        self._negate = negate

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

    def _build_right_value(self) -> int | float | str | Col | Self:
        try:
            return f"({self._right_value.build()})" if self._op == Operator.In else self._right_value.build()
        except AttributeError:
            pass
        return quote_expr(self._right_value)

    def build(self) -> str:
        """ Build the condition """
        return ("NOT" if self._negate else "") + f"({quote_expr(self._left_value)} {self._op.value} {self._build_right_value()})"
