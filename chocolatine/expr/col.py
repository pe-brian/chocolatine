from __future__ import annotations

import re
from typing import Any, Iterable, Self, TYPE_CHECKING



if TYPE_CHECKING:
    from .query import Query

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

from .when import When
from .condition import Condition
from ..sql_type import SqlType
from ..operator import Operator
from ..ordering import Ordering
from ..agg_function import AggFunction
from ..sql_function import SqlFunction


@typechecked
class Col(ChocExpr):
    """ SQL column """
    def __init__(
            self,
            name: str,
            alias: str | None = None,
            agg_function: AggFunction | None = None,
            sql_function: SqlFunction | None = None,
            ordering: Ordering | None = None,
            table_name: str | None = None,
            type: SqlType | None = None
    ) -> None:
        if not name:
            raise ValueError("The name parameter must not be empty")
        if name.startswith("<:"):
            name = name[2:]
            ordering = Ordering.Descending
        elif name.startswith(">:"):
            name = name[2:]
            ordering = Ordering.Ascending
        if name != "*":
            match = re.search(r"^([A-Za-z_\s]+\.)?([A-Za-z_\s()]+){1}((?:@|:)[A-Za-z_\s]*)?$", name)
            if not match:
                raise ValueError(f"Forbidden characters in expr '{name}'")
            r, n, a = match.groups()
            name = n
            alias = alias or (a[1:] if a else None)
            table_name = table_name or (r[:-1] if r else None)
        else:
            if alias:
                raise ValueError("alias parameter can't be used with star expression")
            if table_name:
                raise ValueError("table_name parameter can't be used with star expression")
            if ordering:
                raise ValueError("ordering parameter can't be used with star expression")

        self._agg_function = agg_function
        self._sql_function = sql_function
        self._ordering = ordering
        self._concatenation = []
        self._alias = alias
        self._table_name = table_name
        self._name = name
        self._type = type

        super().__init__("{full_name}@{_alias}: AS {_alias}:;")

    @property
    def full_name(self):
        if self._concatenation:
            name = f"CONCAT({", ".join(list(f"'{x}'" if type(x) is str else str(x) for x in self._concatenation))})"
        else:
            name = f"{self._table_name + "." if self._table_name else ""}{self._name}"
        if self._agg_function:
            return f"{self._agg_function.value}({f"{name}"})"
        if self._sql_function:
            return f"{self._sql_function.value}({f"{name}"})"
        return f"{name}"
    
    @property
    def creation_name(self):
        return f"{self._name} {self._type.value}"

    def copy(self) -> Self:
        """ Copy the column """
        return Col(
            name=self._name,
            alias=self._alias,
            agg_function=self._agg_function,
            sql_function=self._sql_function,
            ordering=self._ordering,
            table_name=self._table_name
        )

    def __gt__(self, value: Col | int | float | When) -> Condition:
        return Condition(left_value=self, op=Operator.GreaterThan, right_value=value)

    def __eq__(self, value: Col | int | float | str | When) -> Condition:
        return Condition(left_value=self, op=Operator.Equal, right_value=value)

    def __ne__(self, value: Col | int | float | str | When) -> Condition:
        return Condition(left_value=self, op=Operator.NotEqual, right_value=value)

    def __and__(self, value: Col | str) -> Self:
        if not self._concatenation:
            self._concatenation.append(self.copy())
        self._sql_function = None
        self._concatenation.append(value)
        return self

    def __rand__(self, value: Col | str) -> Self:
        return self.__and__(value)

    def __rshift__(self, value: str) -> Condition:
        return self.like(value)

    def __lshift__(self, expr: Query | Iterable[int | float | str]) -> Condition:
        return self.isin(expr)

    def order(self, ordering: Ordering = Ordering.Ascending) -> Self:
        """ Order a column """
        self._ordering = ordering
        return self

    def asc(self) -> Self:
        """ Order a column by ascending order """
        return self.order(Ordering.Ascending)

    def desc(self) -> Self:
        """ Order a column by descending order """
        return self.order(Ordering.Descending)

    def like(self, expr: str) -> Condition:
        """ Apply the "like" operator """
        return Condition(self, Operator.Like, expr)

    def isin(self, expr: Query | Iterable[int | float | str]) -> Condition:
        """ Apply the "in" operator """
        return Condition(self, Operator.In, expr)

    def upper(self) -> Self:
        """ Apply the "upper" operator """
        self._sql_function = SqlFunction.Upper
        return self

    def lower(self) -> Self:
        """ Apply the "lower" operator """
        self._sql_function = SqlFunction.Lower
        return self

    def alias(self, name: str) -> Self:
        """ Set an alias """
        if name.startswith("<:"):
            name = name[2:]
            self._ordering = Ordering.Descending
        elif name.startswith(">:"):
            name = name[2:]
            self._ordering = Ordering.Ascending
        self._alias = name
        return self

    def remove_alias(self) -> Self:
        """ Remove the alias """
        self._alias = None
        return self

    def aggregate(self, agg_function: AggFunction) -> Self:
        """ Set an aggregate function """
        self._agg_function = agg_function
        return self

    def sum(self) -> Self:
        """ Apply the "sum" function """
        self._agg_function = AggFunction.Sum
        return self

    def count(self) -> Self:
        """ Apply the "count" function """
        self._agg_function = AggFunction.Count
        return self

    def max(self) -> Self:
        """ Apply the "max" function """
        self._agg_function = AggFunction.Max
        return self

    def min(self) -> Self:
        """ Apply the "min" function """
        self._agg_function = AggFunction.Min
        return self

    def average(self) -> Self:
        """ Apply the "avg" function """
        self._agg_function = AggFunction.Average
        return self

    @property
    def ordering_label(self) -> str | None:
        return f"{(self._table_name + ".") if self._table_name else ""}{self._alias if self._alias else self._name} {self._ordering.value}" if self._ordering else None
