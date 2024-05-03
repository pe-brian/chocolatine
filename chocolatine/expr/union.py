from choc_expr import Expr as ChocExpr


class Union(ChocExpr):

    def __init__(self, left_query, right_query, compact: bool = False) -> None:
        self._left_query = left_query
        self._right_query = right_query
        super().__init__("{_left_query~}UNION~{_right_query}", compact=compact)
