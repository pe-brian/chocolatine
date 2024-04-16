import re

from typeguard import typechecked

from .choc_expr_attr import ChocExprAttr
from .expr import Expr
from ..utils import flatten


@typechecked
class ChocExpr(Expr):
    """ Choc Expr """

    def __init__(
        self,
        choc_expr: str | None = None
    ) -> None:
        self._expr = choc_expr or ""
        # Extract the choc expr attr keys from the choc expr
        self._keys = set(re.findall(r"{([A-Za-z_.$()]+)}", self._expr)) if self._expr else set()
        # Clean the choc expr
        for k, key in enumerate(self._keys):
            self._expr = self._expr.replace(key, f"_{k}")
        # Create the choc expr attributes
        self._mapping = {f"_{k}": ChocExprAttr(self, key) for k, key in enumerate(self._keys)}

    @staticmethod
    def _process(expr: str | None) -> str:
        if not expr:
            return ""
        parts = expr.split("@")
        parts = flatten(list(part.split(";") for part in parts if part))
        parts = list(part.split(":") for part in parts if part)
        res = []
        for part in parts:
            if part[0] == 'False':
                if part[2]:
                    res.append(part[2])
            elif part[0] == 'True':
                if part[1]:
                    res.append(part[1])
            else:
                if part[0]:
                    res.append(part[0])
        return "".join(res)

    def build(self) -> str:
        return ChocExpr._process(self._expr.format(**{k: v.build() for k, v in self._mapping.items()})) if self.buildable else ""
