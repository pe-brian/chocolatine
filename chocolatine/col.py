from typing import Any, Self

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

    def __init__(
            self,
            name: str,
            alias: str | None = None,
            agg_function: AggFunction | None = None,
            sql_function: SqlFunction | None = None,
            ordering: Ordering | None = None,
            ref: str | None = None
    ) -> None:
        super().__init__(name=name, alias=alias, ref=ref)
        self._agg_function = agg_function
        self._sql_function = sql_function
        self._ordering = ordering
        self._concatenation = []

    def copy(self) -> Self:
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
        self._concatenation.append(value)
        return self

    def __rand__(self, value: Any) -> Self:
        return self.__and__(value)

    def order(self, ordering: Ordering = Ordering.Ascending) -> Self:
        self._ordering = ordering
        return self

    def asc(self) -> Self:
        return self.order(Ordering.Ascending)

    def desc(self) -> Self:
        return self.order(Ordering.Descending)

    def like(self, expr: str):
        return Condition(self, Operator.Like, expr)

    def isin(self, *expr: str):
        return Condition(self, Operator.In, expr)

    def upper(self) -> Self:
        self._sql_function = SqlFunction.Upper
        return self

    def lower(self) -> Self:
        self._sql_function = SqlFunction.Lower
        return self

    def alias(self, name: str) -> Self:
        self._alias = name
        return self

    def aggregate(self, agg_function: AggFunction) -> Self:
        self._agg_function = agg_function
        return self

    def sum(self) -> Self:
        self._agg_function = AggFunction.Sum
        return self

    def count(self) -> Self:
        self._agg_function = AggFunction.Count
        return self

    def max(self) -> Self:
        self._agg_function = AggFunction.Max
        return self

    def min(self) -> Self:
        self._agg_function = AggFunction.Min
        return self

    def average(self) -> Self:
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
