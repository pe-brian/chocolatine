from typing import Iterable
from typeguard import typechecked

from .col import Col
from .expr import Expr


@typechecked
class Select(Expr):
    """ Select expression """
    def __init__(
            self,
            cols: Iterable[Col | str] | None = None
    ) -> None:
        self._cols = [Col(col) if type(col) is str else col for col in cols] if cols else [Col("*")]

    def build(self) -> str:
        return f"SELECT {", ".join(str(col) for col in self._cols)}"
