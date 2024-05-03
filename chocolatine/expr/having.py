from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from .condition import Condition


@typechecked
class Having(ChocExpr):
    """ Having expression """
    def __init__(
            self,
            condition: Condition | None = None,
            compact: bool = True
    ) -> None:
        self.condition = condition
        super().__init__("HAVING {condition}", compact=compact)

    @property
    def condition(self) -> Condition | None:
        return self._condition

    @condition.setter
    def condition(self, value: Condition | None) -> None:
        self._condition = value

    @property
    def buildable(self) -> bool:
        return self.condition is not None
