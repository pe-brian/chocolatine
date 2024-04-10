from typing import Iterable, List, Self

from typeguard import typechecked

from chocolatine.operator import Operator

from .agg_function import AggFunction
from .expr import Expr
from .join_type import JoinType
from .condition import Condition
from .col import Col
from .table import Table


@typechecked
class Request(Expr):
    """ Handler to generate a SQL request """
    def __init__(
            self,
            compact: bool = True
    ) -> None:
        self._table = None
        self._selected_cols = []
        self._unique = False
        self._group_by_cols = []
        self._where_condition = []
        self._having_condition = []
        self._joins = []
        self._compact = compact
        self._last_joined_table = None
        self._joined_cols = {}

    def table(self, name: str | Table, alias: str | None = None) -> Self:
        """ Set the table name """
        self._table = Table(name=name, alias=alias) if type(name) is str else name
        return self

    def select(self, *selected_cols: str | Col) -> Self:
        """ Set the selected cols """
        self._selected_cols = [(col if type(col) is Col else Col(col)) for col in selected_cols]
        return self

    def distinct(self) -> Self:
        """ Filter the rows to remove duplicates (by selected columns)"""
        self._unique = True
        return self

    def filter(self, condition: Condition) -> Self:
        """ Filter the rows according to the given condition """
        if any(x in condition.build() for x in set(e.value for e in AggFunction)):
            self._having_condition = condition
        else:
            self._where_condition = condition
        return self

    def group_by(self, *cols_names: str) -> Self:
        """ Group the rows of the specified columns """
        self._group_by_cols = cols_names
        return self

    def join(self, table: str | Table, condition: Condition | str | Iterable[str], joinType: JoinType | None = JoinType.Inner) -> Self:
        """ Join two tables according to the given condition """
        if type(table) is str:
            table = Table(table)
        if not table._alias:
            table.alias()
        if not self._table._alias:
            self._table.alias()

        def _gen_condition(table, other, condition):
            left_table_alias = table._alias if type(table) is Table else Table(table)._alias
            right_table_alias = (other._alias if hasattr(other, "_alias") else None) or self._table._alias
            self._joined_cols[condition] = (left_table_alias, right_table_alias)
            return Col(f"{left_table_alias}.{condition}") == Col(f"{right_table_alias}.{condition}")

        if type(condition) is not Condition:
            if type(condition) is str:
                condition = _gen_condition(table, self._last_joined_table or self._table, condition)
            else:
                if len(condition) < 2:
                    raise ValueError("More conditions are expected")
                for k in range(len(condition)):
                    if k == 0:
                        c = _gen_condition(table, self._table, condition[0])
                    elif k > 0:
                        c = Condition(left_value=_gen_condition(table, self._table, condition[k]), op=Operator.And, right_value=c)
                condition = c
        self._joins.append((table if type(table) is Table else Table(table), joinType, condition))
        self._last_joined_table = table if type(table) is Table else Table(table)
        return self

    def _build_select(self) -> str:
        def _remove_col_ambiguity(col):
            if col._name in self._joined_cols:
                col._ref = self._joined_cols[col._name][0]
            return col
        expr = "SELECT "
        cols = ", ".join(list(_remove_col_ambiguity(col).build() for col in self._selected_cols)) if self._selected_cols else "*"
        expr += f"DISTINCT({cols})" if self._unique else cols
        return expr

    def _build_from(self) -> str:
        return f"FROM {self._table}"

    def _build_where(self) -> str:
        return f"WHERE {self._where_condition}" if self._where_condition else ""

    def _build_group_by(self) -> str:
        return f"GROUP BY {", ".join(self._group_by_cols)}" if self._group_by_cols else ""

    def _build_having(self) -> str:
        return f"HAVING {self._having_condition}" if self._having_condition else ""

    def _build_order_by(self) -> str:
        ordering = []
        for col in self._selected_cols:
            if type(col) is Col and col._ordering is not None:
                ordering.append(f"{col._name} {col._ordering.value}")
        return f"ORDER BY {", ".join(ordering)}" if ordering else ""

    def _build_join(self) -> List[str]:
        exprs = []
        for table, join_type, condition in self._joins:
            exprs.append(f"{join_type.value} JOIN {table}")
            exprs.append(f"ON {condition}")
        return exprs

    def build(self) -> str:
        """ Build the query """
        return f"{" " if self._compact else "\n"}".join(
            part for part in [
                self._build_select(),
                self._build_from(),
                self._build_where(),
                *self._build_join(),
                self._build_group_by(),
                self._build_having(),
                self._build_order_by()
            ] if part
        )
