from chocolatine.agg_function import AggFunction
from chocolatine.col import Col


def count() -> Col:
    return Col(name="*", agg_function=AggFunction.Count)


def sum(col_name: str) -> Col:
    return Col(name=col_name, agg_function=AggFunction.Sum)
