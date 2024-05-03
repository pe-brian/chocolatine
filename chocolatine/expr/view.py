from choc_expr import Expr as ChocExpr

from ..expr.query import Query
from ..view_mode import ViewMode


class View(ChocExpr):

    def __init__(self, name: str, query: Query | None = None, mode=ViewMode.Create, compact: bool = True) -> None:
        self._name = name
        self._query = query
        self._mode = mode
        super().__init__("@{create_mode}:CREATE VIEW {_name} AS~{_query}:;@{drop_mode}:DROP VIEW {_name}~:;", compact=compact)

    @property
    def create_mode(self):
        return self._mode == ViewMode.Create

    @property
    def drop_mode(self):
        return self._mode == ViewMode.Drop
