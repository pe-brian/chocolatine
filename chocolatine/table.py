from .expr import Expr


class Table(Expr):

    def __init__(
            self,
            name: str,
            schema: str = None,
            alias: str = None
    ):
        super().__init__(name=name, alias=alias, ref=schema)
