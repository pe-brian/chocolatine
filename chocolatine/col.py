from typing import Self
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
        self.name = name
        self.new_name = new_name
        self.ref_table = ref_table
        self.agg_function = agg_function
        self.sql_function = sql_function
        self.ordering = ordering
        self.concatenation = []

    def __gt__(self, value) -> Condition:
        return Condition(left_value=self, op=Operator.GreaterThan, right_value=value)

    def __eq__(self, value) -> Condition:
        return Condition(left_value=self, op=Operator.Equal, right_value=value)

    def __ne__(self, value) -> Condition:
        return Condition(left_value=self, op=Operator.NotEqual, right_value=value)

    def __and__(self, value) -> Self:
        self.concatenation.append(value)
        return self

    def __rand__(self, value) -> Self:
        return self.__and__(value)

    def order(self, ordering: Ordering) -> Self:
        self.ordering = ordering
        return self

    def asc(self) -> Self:
        return self.order(Ordering.Ascending)

    def desc(self) -> Self:
        return self.order(Ordering.Descending)

    def upper(self) -> Self:
        self.sql_function = SqlFunction.Upper
        return self

    def lower(self) -> Self:
        self.sql_function = SqlFunction.Lower
        return self

    def alias(self, new_name: str) -> Self:
        self.new_name = new_name
        return self

    def aggregate(self, agg_function: AggFunction) -> Self:
        self.agg_function = agg_function
        return self

    def sum(self) -> Self:
        self.agg_function = AggFunction.Sum
        return self

    def count(self) -> Self:
        self.agg_function = AggFunction.Count
        return self

    def max(self) -> Self:
        self.agg_function = AggFunction.Max
        return self

    def min(self) -> Self:
        self.agg_function = AggFunction.Min
        return self

    def average(self) -> Self:
        self.agg_function = AggFunction.Average
        return self

    def build(self) -> str:
        expr = f"{(self.ref_table + ".") if self.ref_table else ""}{self.name}"
        if self.concatenation:
            copy = Col(name=self.name, sql_function=self.sql_function, ref_table=self.ref_table)
            expr = f"CONCAT({copy}, {", ".join(f"'{x}'" if type(x) is str else str(x) for x in self.concatenation)})"
        else:
            if self.agg_function:
                expr = f"{self.agg_function.value}({expr})"
            if self.sql_function:
                expr = f"{self.sql_function.value}({expr})"
            if self.new_name:
                expr += f" AS {self.new_name}"
        return expr
