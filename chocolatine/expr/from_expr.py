from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from .table import Table


@typechecked
class FromExpr(ChocExpr):
    """ From expression """
    def __init__(
            self,
            table: Table | str | None = None,
            compact: bool = True
    ) -> None:
        self.table = table
        super().__init__("FROM {table}", compact=compact)

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, value):
        self._table = Table(value) if type(value) is str else value

    @property
    def buildable(self) -> bool:
        return self.table is not None
