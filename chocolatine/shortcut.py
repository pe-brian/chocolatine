from typeguard import typechecked

from .agg_function import AggFunction
from .sql_function import SqlFunction
from .expr.col import Col
from .ordering import Ordering


@typechecked
def concat(*cols: Col) -> Col:
    """ Shortcut to concatenate some columns """
    if len(cols) < 2:
        raise ValueError("You cannot concatenate less than two cols")
    res = None
    for k, col in enumerate(cols):
        res = col if k == 0 else res & col
    return res


@typechecked
def count(col_name: str | None = None) -> Col:
    """ Shortcut to create a column and apply the "count" aggregation function """
    return Col(name=col_name or "*", agg_function=AggFunction.Count)


@typechecked
def sum(col_name: str) -> Col:
    """ Shortcut to create a column and apply the "sum" aggregation function """
    return Col(name=col_name, agg_function=AggFunction.Sum)


@typechecked
def upper(col_name: str) -> Col:
    """ Shortcut to create a column and apply the "upper" SQL function """
    return Col(name=col_name, sql_function=SqlFunction.Upper)


@typechecked
def lower(col_name: str) -> Col:
    """ Shortcut to create a column and apply the "upper" SQL function """
    return Col(name=col_name, sql_function=SqlFunction.Lower)


@typechecked
def second(col_name: str) -> Col:
    """ Shortcut to create a column and apply the "second" SQL function """
    return Col(name=col_name, sql_function=SqlFunction.Second)


@typechecked
def minute(col_name: str) -> Col:
    """ Shortcut to create a column and apply the "minute" SQL function """
    return Col(name=col_name, sql_function=SqlFunction.Minute)


@typechecked
def hour(col_name: str) -> Col:
    """ Shortcut to create a column and apply the "hour" SQL function """
    return Col(name=col_name, sql_function=SqlFunction.Hour)


@typechecked
def day(col_name: str) -> Col:
    """ Shortcut to create a column and apply the "day" SQL function """
    return Col(name=col_name, sql_function=SqlFunction.Day)


@typechecked
def month(col_name: str) -> Col:
    """ Shortcut to create a column and apply the "month" SQL function """
    return Col(name=col_name, sql_function=SqlFunction.Month)


@typechecked
def year(col_name: str) -> Col:
    """ Shortcut to create a column and apply the "year" SQL function """
    return Col(name=col_name, sql_function=SqlFunction.Year)


@typechecked
def asc(col_name: str) -> Col:
    """ Shortcut to create a column and apply the ascending ordering """
    return Col(name=col_name, ordering=Ordering.Ascending)


@typechecked
def desc(col_name: str) -> Col:
    """ Shortcut to create a column and apply the descending ordering  """
    return Col(name=col_name, ordering=Ordering.Descending)
