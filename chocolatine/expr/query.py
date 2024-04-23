from typing import Iterable, Self, Tuple

from typeguard import typechecked

from ..query_mode import QueryMode
from .join import Join
from .order_by import OrderBy
from .group_by import GroupBy
from .having import Having
from .where import Where
from .select_from import SelectFrom
from .limit import Limit
from ..agg_function import AggFunction
from .choc_expr import ChocExpr
from ..join_type import JoinType
from .condition import Condition
from .col import Col
from .table import Table
from .update_set import UpdateSet


@typechecked
class Query(ChocExpr):
    """ Handler to generate a SQL query """
    def __init__(
            self,
            query_mode: QueryMode = QueryMode.Read,
            compact: bool = True,
            limit: int | None = None,
            table: str | Table | None = None,
            unique: bool = False,
            joins: Iterable[Tuple[str | Table, Condition | str | Iterable[str]] | Tuple[str | Table, Condition | str | Iterable[str], JoinType | None]] | None = None,
            cols: Iterable[str | Col] | None = None,
            groups: Iterable[str] | None = None,
            filters: Iterable[Condition] | None = None,
            assignations: Iterable[Condition] | None = None
    ) -> None:
        if cols is None:
            cols = []
        if joins is None:
            joins = []
        if groups is None:
            groups = []
        if filters is None:
            filters = []
        if assignations is None:
            assignations = []
        if query_mode == QueryMode.Read and assignations:
            raise ValueError("You cannot have update assignations in read query mode")
        elif query_mode == QueryMode.Update and cols:
            raise ValueError("You cannot have update cols in update query mode")
        self._query_mode = query_mode
        self._select_from = SelectFrom(table=table, unique=unique, compact=False)
        self._order_by = OrderBy(select=self._select_from.select, compact=False)
        self._group_by = GroupBy(compact=False)
        self._limit = Limit(length=limit, compact=False)
        self._where = Where(compact=False)
        self._having = Having(compact=False)
        self._joins = []
        self._compact = compact
        self._update_set = UpdateSet(table=table, assignations=assignations, compact=compact)
        if joins:
            self.join_many(*joins)
        if cols and query_mode == QueryMode.Read:
            self.select(*cols)
        if groups:
            self.group_by(*groups)
        for filter in filters:
            self.filter(filter)
        super().__init__("@{read_mode}:{_select_from~}{$(_joins)~}:{_update_set~};{_where~}@{read_mode}:{_group_by~}{_having~}{_order_by~}{_limit~}:;", list_join_sep="\n", compact=compact)

    @property
    def read_mode(self) -> bool:
        return self._query_mode == QueryMode.Read

    def table(self, val: str | Table | None) -> Self:
        """ Set the table name """
        self._select_from.from_expr.table = val
        return self

    def select(self, *vals: str | Col) -> Self:
        """ Set the selected cols """
        self._select_from.select.cols = vals
        return self

    def update(self, *assignations: Condition) -> Self:
        """ Set the selected cols """
        self._update_set._set.assignations = assignations
        return self

    def distinct(self) -> Self:
        """ Filter the rows to remove duplicates (by selected columns)"""
        self._select_from.select.unique = True
        return self

    def head(self, length: int = 1) -> Self:
        """ Filter on the first N rows """
        self._limit = length
        return self

    def filter(self, condition: Condition) -> Self:
        """ Filter the rows according to the given condition """
        if any(x in condition.build() for x in set(e.value for e in AggFunction)):
            self._having.condition = condition
        else:
            self._where.condition = condition
        return self

    def group_by(self, *cols_names: str) -> Self:
        """ Group the rows of the specified columns """
        self._group_by.cols = cols_names
        return self

    def join(self, table: str | Table, condition: Condition | str | Iterable[str], join_type: JoinType | None = JoinType.Inner) -> Self:
        self._joins.append(Join(table=table if isinstance(table, Table) else Table(name=table), condition=condition, join_type=join_type, compact=self._compact))
        return self

    def join_many(self, *joins_params: Tuple[str | Table, Condition | str | Iterable[str]] | Tuple[str | Table, Condition | str | Iterable[str], JoinType | None]) -> Self:
        for join_params in joins_params:
            self.join(*join_params)
        return self
