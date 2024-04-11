from typing import Iterable, List, Self

from typeguard import typechecked

from .from_expr import FromExpr
from ..operator import Operator
from ..agg_function import AggFunction
from .named_expr import NamedExpr
from ..join_type import JoinType
from .condition import Condition
from .col import Col
from .table import Table


@typechecked
class Request(NamedExpr):
    """ Handler to generate a SQL request """
    def __init__(
            self,
            compact: bool = True,
            limit_to: int | None = None,
            using: bool = False,
            table: str | Table | None = None
    ) -> None:
        self._selected_cols = []
        self._unique = False
        self._group_by_cols = []
        self._where_condition = []
        self._having_condition = []
        self._joins = []
        self._compact = compact
        self._last_joined_table = None
        self._joined_cols = {}
        self._limit = limit_to
        self._using = using
        self._from_expr = None
        if table:
            self.table(table)

    def table(self, name: str | Table | None) -> Self:
        """ Set the table name """
        self._from_expr = FromExpr(name)
        return self

    def select(self, *selected_cols: str | Col) -> Self:
        """ Set the selected cols """
        self._selected_cols = [(col if type(col) is Col else Col(col)) for col in selected_cols]
        return self

    def distinct(self) -> Self:
        """ Filter the rows to remove duplicates (by selected columns)"""
        self._unique = True
        return self

    def head(self, length: int = 1) -> Self:
        """ Filter on the first N rows """
        self._limit = length
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
        if not self._using:
            if not table._alias:
                table.alias()
            if not self._from_expr._table._alias:
                self._from_expr._table.alias()

            def _gen_condition(table, other, condition):
                left_table_alias = table._alias if type(table) is Table else Table(table)._alias
                right_table_alias = (other._alias if hasattr(other, "_alias") else None) or self._from_expr._table._alias
                self._joined_cols[condition] = (left_table_alias, right_table_alias)
                return Col(f"{left_table_alias}.{condition}") == Col(f"{right_table_alias}.{condition}")
            if type(condition) is not Condition:
                if type(condition) is str:
                    condition = _gen_condition(table, self._last_joined_table or self._from_expr._table, condition)
                else:
                    if len(condition) < 2:
                        raise ValueError("More conditions are expected")
                    for k in range(len(condition)):
                        if k == 0:
                            c = _gen_condition(table, self._from_expr._table, condition[0])
                        elif k > 0:
                            c = Condition(left_value=_gen_condition(table, self._from_expr._table, condition[k]), op=Operator.And, right_value=c)
                    condition = c
            self._joins.append((table if type(table) is Table else Table(table), joinType, condition))
        else:
            if type(condition) is Condition:
                raise ValueError("You cannot use a condition for joining two tables in when using mode is enabled")
            self._joins.append((table if type(table) is Table else Table(table), joinType, [condition] if type(condition) is str else condition))
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

    def _build_where(self) -> str:
        return f"WHERE {self._where_condition}" if self._where_condition else ""

    def _build_group_by(self) -> str:
        return f"GROUP BY {", ".join(self._group_by_cols)}" if self._group_by_cols else ""

    def _build_having(self) -> str:
        return f"HAVING {self._having_condition}" if self._having_condition else ""

    def _build_order_by(self) -> str:
        ordering = []
        for col in self._selected_cols:
            if col._ordering is not None:
                ordering.append(f"{(col._ref + ".") if col._ref else ""}{col._alias if col._alias else col._name} {col._ordering.value}")
        return f"ORDER BY {", ".join(ordering)}" if ordering else ""

    def _build_join(self) -> List[str]:
        exprs = []
        for table, join_type, condition in self._joins:
            exprs.append(f"{join_type.value} JOIN {table}")
            if self._using:
                exprs.append(f"USING ({', '.join(condition)})")
            else:
                exprs.append(f"ON {condition}")
        return exprs

    def _build_limit(self) -> str:
        return f"LIMIT {self._limit}" if self._limit else ""

    def build(self) -> str:
        """ Build the query """
        return f"{" " if self._compact else "\n"}".join(
            part for part in [
                self._build_select(),
                self._from_expr.build() if self._from_expr else "",
                *self._build_join(),
                self._build_where(),
                self._build_group_by(),
                self._build_having(),
                self._build_order_by(),
                self._build_limit()
            ] if part
        )
