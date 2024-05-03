from typing import Iterable

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from .col import Col
from ..utils import quote_expr


@typechecked
class ColWhen(ChocExpr):
    """ 'Case When' expression  """
    def __init__(
            self,
            col: Col | str,
            expected_vals: Iterable[str | int | float],
            returned_vals: Iterable[str | int | float],
            else_returned_val: str | int | float | None = None,
            compact: bool = False
    ):
        if len(expected_vals) != len(returned_vals):
            raise ValueError("'conditions' and 'returned_vals' must have the same length")

        if len(returned_vals) == 0:
            raise ValueError("CaseWhen must not be empty")

        self._col = (Col(col) if type(col) is str else col).remove_alias()
        self._when_then_items = [
            f"WHEN {quote_expr(expected_val)} THEN {quote_expr(returned_val)}" for expected_val, returned_val in zip(expected_vals, returned_vals)
        ]
        self._else = f"ELSE {quote_expr(else_returned_val)}" if else_returned_val else ""
        super().__init__("CASE {_col.full_name~}{$(_when_then_items)~}{_else~}END", compact=compact, list_join_sep="\n")
