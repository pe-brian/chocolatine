import re
from typing import Self

from typeguard import typechecked
from choc_expr import Expr as ChocExpr


@typechecked
class Table(ChocExpr):
    """ Represent a SQL table name """

    def __init__(
            self,
            name: str,
            alias: str | None = None,
            schema: str | None = None
    ) -> None:
        if not name:
            raise ValueError("The name parameter must not be empty")
        match = re.search(r"^([A-Za-z_\s]+\.)?([A-Za-z_\s()]+){1}((?:@|:)[A-Za-z_\s]*)?$", name)
        if not match:
            raise ValueError(f"Forbidden characters in expr '{name}'")
        r, n, a = match.groups()
        self._name = n
        self._alias = alias or (a[1:] if a else None)
        self._schema = schema or (r[:-1] if r else None)
        super().__init__("@{_schema}:{_schema}.:;{_name}@{_alias}: AS {_alias}:;")

    def alias(self, name: str) -> Self:
        """ Set an alias """
        self._alias = name
        return self

    @property
    def full_name(self) -> str:
        return str(self).split("AS")[0].strip()
