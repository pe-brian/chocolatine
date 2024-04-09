from chocolatine.agg_function import AggFunction
from chocolatine.col import Col


def count() -> Col:
    """ Shortcut to create a column and apply the "count" aggregation function """
    return Col(name="*", agg_function=AggFunction.Count)


def sum(col_name: str) -> Col:
    """ Shortcut to create a column and apply the "sum" aggregation function """
    return Col(name=col_name, agg_function=AggFunction.Sum)
