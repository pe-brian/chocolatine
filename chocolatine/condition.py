from typing import Any

from .operator import Operator


class Condition:

    def __init__(self, left_value: str, op: Operator, right_value: Any, negate: bool = False):
        self.left_value = left_value
        self.op = op
        self.right_value = right_value
        self.negate = negate

    def __and__(self, other):
        return Condition(left_value=self, op=Operator.And, right_value=other)

    def __rand__(self, other):
        return self.__and__(other)

    def __or__(self, other):
        return Condition(left_value=self, op=Operator.Or, right_value=other)

    def __ror__(self, other):
        return self.__or__(other)

    def __invert__(self):
        return Condition(left_value=self.left_value, op=self.op, right_value=self.right_value, negate=True)

    def build(self):
        return ("NOT" if self.negate else "") + f"({self.left_value} {self.op.value} {self.right_value})"

    def __str__(self):
        return self.build()

    def __expr__(self):
        return self.build()
