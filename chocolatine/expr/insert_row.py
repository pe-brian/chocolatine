from ..utils import quote_expr


class InsertRow:
    """ Wrapper that renders a tuple of values through quote_expr for parameterized query support """

    def __init__(self, values):
        self._values = list(values)

    def __str__(self) -> str:
        return f"({', '.join(str(quote_expr(v)) for v in self._values)})"

    def __repr__(self) -> str:
        return self.__str__()
