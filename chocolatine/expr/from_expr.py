from typeguard import typechecked

from .choc_expr import ChocExpr
from .table import Table


@typechecked
class FromExpr(ChocExpr):
    """ From expression """
    def __init__(
            self,
            table: Table | str
    ) -> None:
        self._table = Table(table) if type(table) is str else table
        super().__init__(
            choc_expr="FROM {table}",
            table=self.table
        )

    @property
    def table(self):
        return self._table
