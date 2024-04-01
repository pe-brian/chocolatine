from .condition import Condition
from .operator import Operator
from .ordering import Ordering
from .agg_function import AggFunction
from .sql_function import SqlFunction


class Col:

    def __init__(self, name: str, new_name: str = None, agg_function: AggFunction = None, sql_function: SqlFunction = None, ordering: Ordering = None, ref_table: str = None):
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

    def __gt__(self, value):
        return Condition(left_value=self, op=Operator.GreaterThan, right_value=value)

    def __eq__(self, value):
        return Condition(left_value=self, op=Operator.Equal, right_value=value)

    def __ne__(self, value):
        return Condition(left_value=self, op=Operator.NotEqual, right_value=value)

    def __and__(self, value):
        self.concatenation.append(value)
        return self

    def __rand__(self, value):
        return self.__and__(value)

    def order(self, ordering: Ordering):
        self.ordering = ordering
        return self

    def asc(self):
        return self.order(Ordering.Ascending)

    def desc(self):
        return self.order(Ordering.Descending)

    def upper(self):
        self.sql_function = SqlFunction.Upper
        return self

    def lower(self):
        self.sql_function = SqlFunction.Lower
        return self

    def alias(self, new_name: str):
        self.new_name = new_name
        return self

    def aggregate(self, agg_function: AggFunction):
        self.agg_function = agg_function
        return self

    def sum(self):
        self.agg_function = AggFunction.Sum
        return self

    def count(self):
        self.agg_function = AggFunction.Count
        return self

    def max(self):
        self.agg_function = AggFunction.Max
        return self

    def min(self):
        self.agg_function = AggFunction.Min
        return self

    def average(self):
        self.agg_function = AggFunction.Average
        return self

    def build(self):
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

    def __str__(self):
        return self.build()

    def __expr__(self):
        return self.build()
