from typeguard import typechecked

from .expr import Expr
from .table import Table


@typechecked
class FromExpr(Expr):
    """ From expression """
    def __init__(
            self,
            table: Table | str
    ) -> None:
        self._table = Table(table) if type(table) is str else table

    def build(self) -> str:
        return f"FROM {self._table}"
