from typing import Self
from .expr import Expr


class Table(Expr):

    def __init__(
            self,
            name: str,
            new_name: str = None
    ):
        self.name = name
        self.new_name = new_name

    def alias(self, new_name: str) -> Self:
        self.new_name = new_name
        return self

    def build(self) -> str:
        expr = self.name
        if self.new_name:
            expr += f" AS {self.new_name}"
        return expr
