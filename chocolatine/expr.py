import re
from typing import Self


class Expr:

    def __init__(self, name: str, alias: str = None, ref: str = None):
        match = re.search(r"^([A-Za-z_\s]+\.)?([A-Za-z_\s]+){1}((?:@|:)[A-Za-z_\s]*)?$", name)
        if not match:
            raise ValueError("Forbidden characters in expr")
        r, n, a = match.groups()
        self._name = n
        self._alias = alias or (a[1:] if a else None)
        self._ref = ref or (r[:-1] if r else None)

    def alias(self, name: str) -> Self:
        self._alias = name
        return self

    def __str__(self):
        return self.build()

    def __expr__(self):
        return self.build()

    def _build_name(self):
        return self._name

    def _build_full_name(self):
        return f"{self._build_ref()}{self._build_name()}"

    def _build_alias(self):
        return (" AS " + self._alias) if self._alias else ""

    def _build_ref(self):
        return (self._ref + ".") if self._ref else ""

    def build(self):
        return f"{self._build_full_name()}{self._build_alias()}"
