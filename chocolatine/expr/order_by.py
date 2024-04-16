from typing import Iterable
from typeguard import typechecked

from .select import Select
from .col import Col
from .choc_expr import ChocExpr


@typechecked
class OrderBy(ChocExpr):
    """ OrderBy expression """
    def __init__(
            self,
            select: Select
    ) -> None:
        self._select = select
        super().__init__("ORDER BY {$(cols).ordering_label}")

    @property
    def cols(self) -> Iterable[Col]:
        return [col for col in self._select.cols if col.ordering_label]

    @property
    def buildable(self) -> bool:
        return len(self.cols) > 0
