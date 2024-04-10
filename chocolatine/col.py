from __future__ import annotations
from typing import Any, Iterable, Self, TYPE_CHECKING

if TYPE_CHECKING:
    from .request import Request

from typeguard import typechecked

from .utils import quote_expr
from .expr import Expr
from .condition import Condition
from .operator import Operator
from .ordering import Ordering
from .agg_function import AggFunction
from .sql_function import SqlFunction


@typechecked
class Col(Expr):
    """ SQL column """
    def __init__(
            self,
            name: str,
            alias: str | None = None,
            agg_function: AggFunction | None = None,
            sql_function: SqlFunction | None = None,
            ordering: Ordering | None = None,
            ref: str | None = None
    ) -> None:
        if not name:
            raise ValueError("The name parameter must not be empty")
        if name.startswith("<:"):
            name = name[2:]
            ordering = Ordering.Descending
        elif name.startswith(">:"):
            name = name[2:]
            ordering = Ordering.Ascending
        super().__init__(name=name, alias=alias, ref=ref)
        self._agg_function = agg_function
        self._sql_function = sql_function
        self._ordering = ordering
        self._concatenation = []

    def copy(self) -> Self:
        """ Copy the column """
        return Col(
            name=self._name,
            alias=self._alias,
            agg_function=self._agg_function,
            sql_function=self._sql_function,
            ordering=self._ordering,
            ref=self._ref
        )

    def __gt__(self, value: Any) -> Condition:
        return Condition(left_value=self, op=Operator.GreaterThan, right_value=value)

    def __eq__(self, value: Any) -> Condition:
        return Condition(left_value=self, op=Operator.Equal, right_value=value)

    def __ne__(self, value: Any) -> Condition:
        return Condition(left_value=self, op=Operator.NotEqual, right_value=value)

    def __and__(self, value: Any) -> Self:
        if not self._concatenation:
            self._concatenation.append(self.copy())
        self._sql_function = None
        self._concatenation.append(value)
        return self

    def __rand__(self, value: Any) -> Self:
        return self.__and__(value)

    def __rshift__(self, value: str) -> Condition:
        return self.like(value)

    def __lshift__(self, expr: Request | Iterable[Any]) -> Condition:
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

    def like(self, expr: str):
        """ Apply the "like" operator """
        return Condition(self, Operator.Like, expr)

    def isin(self, expr: Request | Iterable[Any]):
        """ Apply the "in" operator """
        try:
            expr = expr.build()
        except AttributeError:
            pass
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

    def _build_concat(self) -> str:
        return f"CONCAT({", ".join(quote_expr(x) if type(x) is str else str(x) for x in self._concatenation)})"

    def _build_function(self) -> str:
        if self._agg_function:
            return f"{self._agg_function.value}({"{}"})"
        if self._sql_function:
            return f"{self._sql_function.value}({"{}"})"
        return "{}"

    def _build_full_name(self) -> str:
        return self._build_function().format(super()._build_full_name() if not self._concatenation else self._build_concat())
