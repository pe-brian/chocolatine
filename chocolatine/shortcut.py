from typeguard import typechecked

from .agg_function import AggFunction
from .sql_function import SqlFunction
from .expr.col import Col
from .ordering import Ordering


@typechecked
def count() -> Col:
    """ Shortcut to create a column and apply the "count" aggregation function """
    return Col(name="*", agg_function=AggFunction.Count)


@typechecked
def sum(col_name: str) -> Col:
    """ Shortcut to create a column and apply the "sum" aggregation function """
    return Col(name=col_name, agg_function=AggFunction.Sum)


@typechecked
def asc(col_name: str) -> Col:
    """ Shortcut to create a column and apply the ascending ordering """
    return Col(name=col_name, ordering=Ordering.Ascending)


@typechecked
def desc(col_name: str) -> Col:
    """ Shortcut to create a column and apply the descending ordering  """
    return Col(name=col_name, ordering=Ordering.Descending)


@typechecked
def upper(col_name: str) -> Col:
    """ Shortcut to create a column and apply the "upper" SQL function """
    return Col(name=col_name, sql_function=SqlFunction.Upper)


@typechecked
def lower(col_name: str) -> Col:
    """ Shortcut to create a column and apply the "upper" SQL function """
    return Col(name=col_name, sql_function=SqlFunction.Lower)


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
