from typeguard import typechecked

from .choc_expr import ChocExpr


@typechecked
class Delete(ChocExpr):
    """ Delete expression """
    def __init__(
            self,
            compact: bool = True
    ) -> None:
        super().__init__("DELETE", compact=compact)
