from .condition import Condition
from .operator import Operator
from .ordering import Ordering
from .agg_function import AggFunction


class Col:

    def __init__(self, name: str, new_name: str = None, aggregation_op: AggFunction = None, ordering: Ordering = None):
        self.name = name
        self.new_name = new_name
        self.aggregation_op = aggregation_op
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

    def aggregate(self, aggregation_op: AggFunction):
        self.aggregation_op = aggregation_op
        return self

    def sum(self):
        self.aggregation_op = AggFunction.Sum
        return self

    def build(self):
        expr = self.name
        if self.aggregation_op:
            expr = f"{self.aggregation_op.value}({expr})"
        if self.new_name:
            expr += f" AS {self.new_name}"
        return expr

    def __str__(self):
        return self.build()

    def __expr__(self):
        return self.build()
