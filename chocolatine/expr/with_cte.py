from __future__ import annotations

from typing import Iterable, Tuple, TYPE_CHECKING

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

if TYPE_CHECKING:
    from .query import Query


@typechecked
class With(ChocExpr):
    """
    CTE (Common Table Expression) — WITH ... AS (...) SELECT ...

    Supports multiple CTEs and the RECURSIVE modifier.
    """

    def __init__(
            self,
            ctes: Iterable[Tuple[str, Query]],
            query: Query,
            recursive: bool = False,
            compact: bool = True
    ) -> None:
        """
        Build a WITH clause followed by a main query.

        :param ctes: Ordered list of (name, query) pairs defining each CTE.
        :param query: The main query that references the CTEs.
        :param recursive: If True, add the RECURSIVE modifier.
        :param compact: If True, render on a single line.
        """
        self._ctes = list(ctes)
        if not self._ctes:
            raise ValueError("With requires at least one CTE")
        self._query = query
        self._recursive = recursive
        self._compact = compact
        super().__init__("{_cte_clause}~{_query}", compact=compact)

    @property
    def _cte_clause(self) -> str:
        keyword = "WITH RECURSIVE" if self._recursive else "WITH"
        if self._compact:
            items = ", ".join(f"{name} AS ({q.build()})" for name, q in self._ctes)
            return f"{keyword} {items}"
        else:
            items = ",\n".join(f"{name} AS (\n{q.build()}\n)" for name, q in self._ctes)
            return f"{keyword}\n{items}"
