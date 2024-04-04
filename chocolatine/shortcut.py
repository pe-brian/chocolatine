from chocolatine.agg_function import AggFunction
from chocolatine.col import Col


def count():
    return Col(name="*", agg_function=AggFunction.Count)
