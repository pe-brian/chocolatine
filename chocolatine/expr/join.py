from typing import Iterable

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from ..enums.join_type import JoinType
from .table import Table
from .condition import Condition


@typechecked
class Join(ChocExpr):
    """ Select expression """
    def __init__(
            self,
            table: Table,
            condition: Condition | str | Iterable[str] | None = None,
            join_type: JoinType = JoinType.Inner,
            compact: bool = True
    ) -> None:
        self._table = table
        self._join_type = join_type
        if condition is None:
            self._condition = None
            self._using = False
            super().__init__("{_join_type.value} JOIN {_table}", compact=compact)
        else:
            if isinstance(condition, str):
                condition = [condition]
            self._condition = condition
            self._using = not isinstance(condition, Condition)
            super().__init__("{_join_type.value} JOIN {_table~}@{_using}:USING {$(_condition)}:ON {_condition};", compact=compact)
