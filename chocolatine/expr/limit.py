from typeguard import typechecked

from .choc_expr import ChocExpr


@typechecked
class Limit(ChocExpr):
    """ Limit expression """
    def __init__(
            self,
            length: int
    ) -> None:
        if length < 1:
            raise ValueError("Length cannot be lower than 1")
        self._length = length
        super().__init__(
            choc_expr="LIMIT {length}"
        )

    @property
    def length(self) -> int:
        return self._length
