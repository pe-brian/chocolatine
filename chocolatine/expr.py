import re
from typing import Self

from typeguard import typechecked


@typechecked
class Expr:

    def __init__(self, name: str, alias: str | None = None, ref: str | None = None) -> None:
        if name != "*":
            match = re.search(r"^([A-Za-z_\s]+\.)?([A-Za-z_\s]+){1}((?:@|:)[A-Za-z_\s]*)?$", name)
            if not match:
                raise ValueError(f"Forbidden characters in expr '{name}'")
            r, n, a = match.groups()
            self._name = n
            self._alias = alias or (a[1:] if a else None)
            self._ref = ref or (r[:-1] if r else None)
        else:
            self._name = name
            self._alias = alias
            if ref:
                raise ValueError("Ref parameter can't be used with when name is *")
            self._ref = ref

    def alias(self, name: str) -> Self:
        self._alias = name
        return self

    def __str__(self) -> str:
        return self.build()

    def __expr__(self) -> str:
        return self.build()

    def _build_name(self) -> str:
        return self._name

    def _build_full_name(self) -> str:
        return f"{self._build_ref()}{self._build_name()}"

    def _build_alias(self) -> str:
        return (" AS " + self._alias) if self._alias else ""

    def _build_ref(self) -> str:
        return (self._ref + ".") if self._ref else ""

    def build(self) -> str:
        return f"{self._build_full_name()}{self._build_alias()}"
