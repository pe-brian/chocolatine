import abc

from typeguard import typechecked

from ..utils import proc_chocolang


@typechecked
class ChocExpr(metaclass=abc.ABCMeta):
    """ Expression """

    def __init__(self, choc_expr: str | None = None, **kwargs) -> None:
        self.choc_expr = None if choc_expr == "" else choc_expr.format(**kwargs)

    def __str__(self) -> str:
        return self.build()

    def __expr__(self) -> str:
        return self.build()

    def build(self) -> str:
        """ Build the expression """
        return proc_chocolang(self.choc_expr)
