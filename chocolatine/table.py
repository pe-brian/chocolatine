from typeguard import typechecked

from .expr import Expr


@typechecked
class Table(Expr):
    """ SQL table """
    def __init__(
            self,
            name: str,
            schema: str | None = None,
            alias: str | None = None
    ):
        super().__init__(name=name, alias=alias, ref=schema)
