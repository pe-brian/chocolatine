import abc


class Expr(metaclass=abc.ABCMeta):

    def __str__(self):
        return self.build()

    def __expr__(self):
        return self.build()

    @abc.abstractmethod
    def build(self):
        pass
