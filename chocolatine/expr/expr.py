from abc import ABC, abstractmethod


class Expr(ABC):
    """ Expression """

    def __str__(self) -> str:
        return self.build()

    def __expr__(self) -> str:
        return self.build()

    @property
    def buildable(self) -> bool:
        return True

    @abstractmethod
    def build(self) -> str:
        pass
