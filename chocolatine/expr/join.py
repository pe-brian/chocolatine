from typing import Iterable

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from ..join_type import JoinType
from .table import Table
from .condition import Condition


@typechecked
class Join(ChocExpr):
    """ Select expression """
    def __init__(
            self,
            table: Table,
            condition: Condition | str | Iterable[str],
            join_type: JoinType = JoinType.Inner,
            compact: bool = True
    ) -> None:
        if isinstance(condition, str):
            condition = [condition]
        self._table = table
        self._condition = condition
        self._join_type = join_type
        self._using = not isinstance(condition, Condition)
        super().__init__("{_join_type.value} JOIN {_table~}@{_using}:USING {$(_condition)}:ON {_condition};", compact=compact)
