import abc

from typeguard import typechecked


@typechecked
class Expr(metaclass=abc.ABCMeta):
    """ Expression """

    def __str__(self) -> str:
        return self.build()

    def __expr__(self) -> str:
        return self.build()

    @abc.abstractmethod
    def build(self) -> str:
        """ Build the expression """
        pass
