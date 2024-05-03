from typeguard import typechecked
from choc_expr import Expr as ChocExpr


@typechecked
class Limit(ChocExpr):
    """ Limit expression """
    def __init__(
            self,
            length: int | None,
            compact: bool = True
    ) -> None:
        if length is not None and length < 1:
            raise ValueError("Length cannot be lower than 1")
        self._length = length
        super().__init__("LIMIT {length}", compact=compact)

    @property
    def length(self) -> int:
        return self._length

    @property
    def buildable(self) -> bool:
        return self._length is not None and self._length > 0
