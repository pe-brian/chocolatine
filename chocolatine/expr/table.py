from typeguard import typechecked

from .named_expr import NamedExpr


@typechecked
class Table(NamedExpr):
    """ SQL table """
    def __init__(
            self,
            name: str,
            schema: str | None = None,
            alias: str | None = None
    ):
        super().__init__(name=name, alias=alias, ref=schema)
