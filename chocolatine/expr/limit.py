from typeguard import typechecked

from .expr import Expr


@typechecked
class Limit(Expr):
    """ Limit expression """
    def __init__(
            self,
            length: int
    ) -> None:
        if length < 1:
            raise ValueError("Length cannot be lower than 1")
        self._length = length

    def build(self) -> str:
        return f"LIMIT {self._length}"
