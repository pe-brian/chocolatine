from typeguard import typechecked

from .select import Select
from .choc_expr import ChocExpr


@typechecked
class OrderBy(ChocExpr):
    """ OrderBy expression """
    def __init__(
            self,
            select: Select
    ) -> None:
        self._select = select
        super().__init__("ORDER BY {$ordered_cols.ordering_label}")

    @property
    def ordered_cols(self):
        return [col for col in self._select.cols if col]
