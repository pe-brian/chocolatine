from typing import Any, Iterable, Self, Tuple

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from .delete_from import DeleteFrom
from ..query_mode import QueryMode
from ..alter_mode import AlterMode
from .join import Join
from .order_by import OrderBy
from .group_by import GroupBy
from .having import Having
from .where import Where
from .select_from import SelectFrom
from .limit import Limit
from ..agg_function import AggFunction
from ..join_type import JoinType
from .condition import Condition
from .col import Col
from .table import Table
from .update_set import UpdateSet
from .union import Union


@typechecked
class Query(ChocExpr):
    """ Handler to generate a SQL query """

    def __init__(
            self,
            query_mode: QueryMode = QueryMode.Select,
            compact: bool = True,
            limit: int | None = None,
            table: str | Table | None = None,
            unique: bool = False,
            joins: Iterable[Tuple[str | Table, Condition | str | Iterable[str]] | Tuple[str | Table, Condition | str | Iterable[str], JoinType | None]] | None = None,
            cols: Iterable[str | Col] | None = None,
            groups: Iterable[str] | None = None,
            filters: Iterable[Condition] | None = None,
            assignations: Iterable[Condition] | None = None,
            values: Iterable[Iterable[Any]] | None = None,
            auto_id: bool = False,
            alter_mode: AlterMode | None = None,
            alter_col: Col | str | None = None,
            alter_new_col: Col | str | None = None,
            alter_col_after: Col | str | None = None
    ) -> None:
        """"""
        self._compact = compact
        self._query_mode = query_mode
        self._table = table
        match query_mode:
            case QueryMode.Create:
                self._auto_id = auto_id
                if cols is None:
                    cols = []
                self._cols = cols
                super().__init__(
                    "CREATE TABLE {_table}~(@{_auto_id}:id MEDIUMINT NOT NULL AUTO_INCREMENT, :;{$(_cols).creation_name}@{_auto_id}:, PRIMARY KEY (id):;)",
                    compact=compact
                )
            case QueryMode.Insert:
                if cols is None:
                    cols = []
                self._cols = cols
                if values is None:
                    values = []
                self._values = values
                super().__init__(
                    "INSERT INTO {_table} ({$(_cols)})~VALUES {$(_values)}",
                    compact=compact
                )
            case QueryMode.Alter:
                self._alter_mode = alter_mode
                if isinstance(alter_col, str):
                    alter_col = Col(alter_col)
                if isinstance(alter_col_after, str):
                    alter_col_after = Col(alter_col_after)
                if isinstance(alter_new_col, str):
                    alter_new_col = Col(alter_new_col)
                self._alter_col = alter_col
                self._alter_col_after = alter_col_after
                self._alter_new_col = alter_new_col
                match alter_mode:
                    case AlterMode.Add:
                        super().__init__(
                            "ALTER TABLE {_table}~ADD COLUMN {_alter_new_col.creation_name}@{_alter_col_after}: AFTER {_alter_col_after}:;~",
                            compact=compact
                        )
                    case AlterMode.Drop:
                        super().__init__(
                            "ALTER TABLE {_table}~DROP COLUMN {_alter_col}~",
                            compact=compact
                        )
                    case AlterMode.Rename:
                        super().__init__(
                            "ALTER TABLE {_table}~RENAME COLUMN {_alter_col} {_alter_new_col}~",
                            compact=compact
                        )
                    case AlterMode.Change:
                        super().__init__(
                            "ALTER TABLE {_table}~CHANGE COLUMN {_alter_col} {_alter_new_col.creation_name}~",
                            compact=compact
                        )
            case QueryMode.Delete:
                self._delete_from = DeleteFrom(table=table, compact=compact)
                if filters is None:
                    filters = []
                self._where = Where(condition=filters[0], compact=False)
                for filter in filters:
                    self.filter(filter)
                for filter in filters:
                    self.filter(filter)
                super().__init__(
                    "{_delete_from~}{_where~}",
                    list_join_sep="\n",
                    compact=compact
                )
            case QueryMode.Update:
                self._update_set = UpdateSet(table=table, assignations=assignations or [], compact=compact)
                self._where = Where(compact=False)
                if filters is None:
                    filters = []
                for filter in filters:
                    self.filter(filter)
                super().__init__(
                    "{_update_set~}{_where~}",
                    list_join_sep="\n",
                    compact=compact
                )
            case QueryMode.Select:
                if cols is None:
                    cols = []
                self._select_from = SelectFrom(table=table, unique=unique, compact=False)
                self.select(*cols)
                self._joins = []
                if joins is None:
                    joins = []
                if joins:
                    self.join_many(*joins)
                self._order_by = OrderBy(select=self._select_from.select, compact=False)
                if groups is None:
                    groups = []
                self._group_by = GroupBy(compact=False)
                if groups:
                    self.group_by(*groups)
                self._limit = Limit(length=limit, compact=False)
                self._where = Where(compact=False)
                if filters is None:
                    filters = []
                self._having = Having(compact=False)
                for filter in filters:
                    self.filter(filter)
                super().__init__(
                    "{_select_from~}{$(_joins)~}{_where~}{_group_by~}{_having~}{_order_by~}{_limit~}",
                    list_join_sep="\n",
                    compact=compact
                )

    @staticmethod
    def alter_table(
        table: str | Table,
        alter_mode: AlterMode,
        col: Col | str | None = None,
        new_col: Col | str | None = None,
        after: Col | str | None = None,
        compact: bool = True
    ):
        """"""
        return Query(query_mode=QueryMode.Alter, alter_mode=alter_mode, table=table, alter_col=col, alter_new_col=new_col, alter_col_after=after, compact=compact)
    
    @staticmethod
    def add_col(
        table: str | Table,
        col: Col,
        after: Col | str | None = None,
        compact: bool = True
    ):
        """"""
        return Query.alter_table(table=table, alter_mode=AlterMode.Add, new_col=col, after=after, compact=compact)
    
    @staticmethod
    def rename_col(
        table: str | Table,
        col: Col | str,
        new_col: Col | str,
        compact: bool = True
    ):
        """"""
        return Query.alter_table(table=table, alter_mode=AlterMode.Rename, col=col, new_col=new_col, compact=compact)
    
    @staticmethod
    def change_col(
        table: str | Table,
        col: Col | str,
        new_col: Col | str,
        compact: bool = True
    ):
        """"""
        return Query.alter_table(table=table, alter_mode=AlterMode.Change, col=col, new_col=new_col, compact=compact)
    
    @staticmethod
    def drop_col(
        table: str | Table,
        col: Col | str,
        compact: bool = True
    ):
        """"""
        return Query.alter_table(table=table, alter_mode=AlterMode.Drop, col=col, compact=compact)
    
    @staticmethod
    def insert_row(
        table: str | Table,
        cols: Iterable[Col],
        row: Iterable[Any],
        compact: bool = True
    ):
        """"""
        return Query(query_mode=QueryMode.Insert, table=table, cols=cols, values=(row,), compact=compact)
    
    @staticmethod
    def insert_rows(
        table: str | Table,
        cols: Iterable[Col],
        rows: Iterable[Iterable[Any]],
        compact: bool = True
    ):
        """"""
        return Query(query_mode=QueryMode.Insert, table=table, cols=cols, values=rows, compact=compact)
    
    @staticmethod
    def delete_rows(table: str | Table, filter: Condition, compact: bool = True):
        """"""
        return Query(query_mode=QueryMode.Delete, table=table, filters=[filter], compact=compact)
    
    @staticmethod
    def get_row(
        table: str | Table,
        unique: bool = False,
        joins: Iterable[Tuple[str | Table, Condition | str | Iterable[str]] | Tuple[str | Table, Condition | str | Iterable[str], JoinType | None]] | None = None,
        cols: Iterable[str | Col] | None = None,
        groups: Iterable[str] | None = None,
        filters: Iterable[Condition] | None = None,
        compact: bool = True
    ):
        """"""
        return Query.get_rows(table=table, limit=1, unique=unique, joins=joins, cols=cols, groups=groups, filters=filters, compact=compact)
    
    @staticmethod
    def get_rows(
        table: str | Table,
        limit: int | None = None,
        unique: bool = False,
        joins: Iterable[Tuple[str | Table, Condition | str | Iterable[str]] | Tuple[str | Table, Condition | str | Iterable[str], JoinType | None]] | None = None,
        cols: Iterable[str | Col] | None = None,
        groups: Iterable[str] | None = None,
        filters: Iterable[Condition] | None = None,
        compact: bool = True
    ):
        """"""
        return Query(query_mode=QueryMode.Select, table=table, limit=limit, unique=unique, joins=joins, cols=cols, groups=groups, filters=filters, compact=compact)
    
    @staticmethod
    def update_rows(table: str | Table, filter: Iterable[Condition], assignations: Iterable[Condition], compact: bool = True):
        """"""
        return Query(query_mode=QueryMode.Delete, table=table, filters=[filter], assignations=assignations, compact=compact)
    
    @staticmethod
    def create_table(table: str | Table, cols: Iterable[Col], auto_id: bool = False, compact: bool = True):
        """"""
        return Query(query_mode=QueryMode.Create, table=table, cols=cols, auto_id=auto_id, compact=compact)

    def compact(self):
        """"""
        self._compact = True

    @property
    def read_mode(self) -> bool:
        return self._query_mode == QueryMode.Select

    @property
    def update_mode(self) -> bool:
        return self._query_mode == QueryMode.Update

    @property
    def delete_mode(self) -> bool:
        return self._query_mode == QueryMode.Delete

    def table(self, val: str | Table | None) -> Self:
        """ Set the table name """
        self._select_from.from_expr.table = val
        return self

    def select(self, *vals: str | Col) -> Self:
        """ Set the selected cols """
        self._select_from.select.cols = vals
        return self

    def update(self, *assignations: Condition) -> Self:
        """ Update """
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
        """ Join two tables together """
        self._joins.append(Join(table=table if isinstance(table, Table) else Table(name=table), condition=condition, join_type=join_type, compact=self._compact))
        return self

    def join_many(self, *joins_params: Tuple[str | Table, Condition | str | Iterable[str]] | Tuple[str | Table, Condition | str | Iterable[str], JoinType | None]) -> Self:
        """ Join more than two tables together """
        for join_params in joins_params:
            self.join(*join_params)
        return self

    def union(self, other_request: Self) -> Union:
        return Union(self, other_request, compact=self._compact)

    def __and__(self, other_request: Self) -> Union:
        return self.union(other_request)

    def __rand__(self, other_request: Self) -> Union:
        return self.__and__(other_request)
