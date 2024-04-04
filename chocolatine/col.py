from typing import Any, Self

from .utils import quote_expr
from .expr import Expr
from .condition import Condition
from .operator import Operator
from .ordering import Ordering
from .agg_function import AggFunction
from .sql_function import SqlFunction


class Col(Expr):

    def __init__(
            self,
            name: str,
            new_name: str = None,
            agg_function: AggFunction = None,
            sql_function: SqlFunction = None,
            ordering: Ordering = None,
            ref_table: str = None
    ):
        if "." in str(name):
            parts = name.split(".")
            if len(parts) != 2:
                raise Exception("Unable to resolve the col name")
            (ref_table, name) = parts
        self._name = name
        self._new_name = new_name
        self._ref_table = ref_table
        self._agg_function = agg_function
        self._sql_function = sql_function
        self._ordering = ordering
        self._concatenation = []

    def copy(self):
        return Col(
            name=self._name,
            new_name=self._new_name,
            agg_function=self._agg_function,
            sql_function=self._sql_function,
            ordering=self._ordering,
            ref_table=self._ref_table
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

    def order(self, ordering: Ordering) -> Self:
        self._ordering = ordering
        return self

    def asc(self) -> Self:
        return self.order(Ordering.Ascending)

    def desc(self) -> Self:
        return self.order(Ordering.Descending)

    def upper(self) -> Self:
        self._sql_function = SqlFunction.Upper
        return self

    def lower(self) -> Self:
        self._sql_function = SqlFunction.Lower
        return self

    def alias(self, new_name: str) -> Self:
        self._new_name = new_name
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

    def build_concat(self) -> str:
        return f"CONCAT({", ".join(quote_expr(x) if type(x) is str else str(x) for x in self._concatenation)})"

    def build(self) -> str:
        expr = f"'{(self._ref_table + ".") if self._ref_table else ""}{self._name}'"
        if self._concatenation:
            expr = self.build_concat()
        if self._agg_function:
            expr = f"{self._agg_function.value}({expr})"
        if self._sql_function:
            expr = f"{self._sql_function.value}({expr})"
        if self._new_name:
            expr += f" AS '{self._new_name}'"
        return expr
