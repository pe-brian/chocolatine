from typeguard import typechecked

from .condition import Condition
from .choc_expr import ChocExpr


@typechecked
class Having(ChocExpr):
    """ Having expression """
    def __init__(
            self,
            condition: Condition | None = None
    ) -> None:
        self.condition = condition
        super().__init__("HAVING {condition}")

    @property
    def condition(self) -> Condition | None:
        return self._condition

    @condition.setter
    def condition(self, value: Condition | None) -> None:
        self._condition = value
