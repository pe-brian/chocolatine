from .condition import Condition
from .operator import Operator
from .ordering import Ordering
from .agg_function import AggFunction


class Col:

    def __init__(self, name: str, new_name: str = None, agg_function: AggFunction = None, ordering: Ordering = None):
        self.name = name
        self.new_name = new_name
        self.agg_function = agg_function
        self.ordering = ordering

    def __gt__(self, value):
        return Condition(left_value=self.name, op=Operator.GreaterThan, right_value=value)

    def __eq__(self, value):
        return Condition(left_value=self.name, op=Operator.Equal, right_value=value)

    def __ne__(self, value):
        return Condition(left_value=self.name, op=Operator.NotEqual, right_value=value)

    def order(self, ordering: Ordering):
        self.ordering = ordering
        return self

    def asc(self):
        return self.order(Ordering.Ascending)

    def desc(self):
        return self.order(Ordering.Descending)

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
        expr = self.name
        if self.agg_function:
            expr = f"{self.agg_function.value}({expr})"
        if self.new_name:
            expr += f" AS {self.new_name}"
        return expr

    def __str__(self):
        return self.build()

    def __expr__(self):
        return self.build()
