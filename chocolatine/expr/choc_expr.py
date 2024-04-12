import re
from typing import Any

from typeguard import typechecked

from ..utils import proc_chocolang


@typechecked
class ChocExpr:
    """ Expression """

    def __init__(
        self,
        choc_expr: str | None = None
    ) -> None:
        self._choc_expr = None if choc_expr == "" else choc_expr
        self._attr_keys = set(re.findall(r"{([A-Za-z_$]+)}", self._choc_expr)) if self._choc_expr else set()

    def __str__(self) -> str:
        return self.build()

    def __expr__(self) -> str:
        return self.build()

    def _get_attr_value(self, key: str) -> Any:
        if key.startswith("$"):
            val = getattr(self, key[1:])
            if val is None:
                raise ValueError("Choc expression contains a None value")
            return ", ".join(str(x) for x in val)
        val = getattr(self, key)
        if val is None:
            raise ValueError("Choc expression contains a None value")
        return val

    def build(self) -> str:
        """ Build the expression """
        return proc_chocolang(
            self._choc_expr.format(
                **{attr_key: self._get_attr_value(attr_key) for attr_key in self._attr_keys}))
