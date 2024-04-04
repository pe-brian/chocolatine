from typing import Self

from .utils import quote_expr
from .expr import Expr


class Table(Expr):

    def __init__(
            self,
            name: str,
            new_name: str = None
    ):
        self._name = name
        self._new_name = new_name

    def alias(self, new_name: str) -> Self:
        self._new_name = new_name
        return self

    def build(self) -> str:
        expr = quote_expr(self._name)
        if self._new_name:
            expr += f" AS '{self._new_name}'"
        return expr
