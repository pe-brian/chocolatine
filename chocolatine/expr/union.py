from choc_expr import Expr as ChocExpr


class Union(ChocExpr):

    def __init__(self, left_query, right_query, all: bool = False, compact: bool = False) -> None:
        self._left_query = left_query
        self._right_query = right_query
        self._all = all
        super().__init__("{_left_query~}{_union_keyword}~{_right_query}", compact=compact)

    @property
    def _union_keyword(self) -> str:
        return "UNION ALL" if self._all else "UNION"
