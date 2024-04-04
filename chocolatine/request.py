from typing import Self

from .expr import Expr
from .join_type import JoinType
from .condition import Condition
from .col import Col
from .table import Table


class Request(Expr):

    def __init__(
            self,
            compact: bool = True
    ):
        self._table = None
        self._selected_cols = []
        self._unique = False
        self._group_by_cols = []
        self._where_condition = []
        self._having_condition = []
        self._joins = []
        self._compact = compact

    def table(self, table_name: str, table_new_name: str = None) -> Self:
        self._table = Table(table_name, table_new_name)
        return self

    def select(self, *selected_cols) -> Self:
        self._selected_cols = selected_cols
        return self

    def distinct(self) -> Self:
        self._unique = True
        return self

    def filter(self, where_condition: Condition = None, having_condition: Condition = None) -> Self:
        if where_condition is None and having_condition is None:
            raise Exception("At least one of where or having condition must be specified")
        self._where_condition = where_condition
        self._having_condition = having_condition
        return self

    def group_by(self, *cols) -> Self:
        self._group_by_cols = cols
        return self

    def join(self, table: str, joinType: JoinType, condition: Condition) -> Self:
        self._joins.append((table, joinType, condition))
        return self

    def build_select(self) -> str:
        expr = "SELECT "
        cols = ", ".join(list(col if type(col) is str else col.build() for col in self._selected_cols)) if self._selected_cols else "*"
        expr += f"DISTINCT({cols})" if self._unique else cols
        return expr

    def build_from(self) -> str:
        return f"FROM {self._table}"

    def build_where(self) -> str:
        return f"WHERE {self._where_condition}" if self._where_condition else ""

    def build_group_by(self) -> str:
        return f"GROUP BY {", ".join(self._group_by_cols)}" if self._group_by_cols else ""

    def build_having(self) -> str:
        return f"HAVING {self._having_condition}" if self._having_condition else ""

    def build_order_by(self) -> str:
        ordering = []
        for col in self._selected_cols:
            if type(col) is Col and col._ordering is not None:
                ordering.append(f"{col._name} {col._ordering.value}")
        return f"ORDER BY {", ".join(ordering)}" if ordering else ""

    def build_join(self) -> str:
        exprs = []
        for table, join_type, condition in self._joins:
            exprs.append(f"{join_type.value} JOIN {table}")
            exprs.append(f"ON {condition}")
        return exprs

    def build(self) -> str:
        return f"{" " if self._compact else "\n"}".join(
            part for part in [
                self.build_select(),
                self.build_from(),
                self.build_where(),
                *self.build_join(),
                self.build_group_by(),
                self.build_having(),
                self.build_order_by()
            ] if part
        )
