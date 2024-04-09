from typing import Any, Self

from typeguard import typechecked

from .utils import quote_expr
from .expr import Expr
from .operator import Operator


@typechecked
class Condition(Expr):

    def __init__(self, left_value: Any, op: Operator, right_value: Any, negate: bool = False) -> None:
        self._left_value = left_value
        self._op = op
        self._right_value = right_value
        self._negate = negate

    def __and__(self, other) -> Self:
        return Condition(left_value=self, op=Operator.And, right_value=other)

    def __rand__(self, other) -> bool:
        return self.__and__(other)

    def __or__(self, other) -> Self:
        return Condition(left_value=self, op=Operator.Or, right_value=other)

    def __ror__(self, other) -> bool:
        return self.__or__(other)

    def __invert__(self) -> Self:
        return Condition(left_value=self._left_value, op=self._op, right_value=self._right_value, negate=True)

    def build(self) -> str:
        return ("NOT" if self._negate else "") + f"({quote_expr(self._left_value)} {self._op.value} {quote_expr(self._right_value)})"
