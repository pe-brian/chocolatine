from __future__ import annotations

from typing import Iterable, Self, TYPE_CHECKING

from typeguard import typechecked
from choc_expr import Expr as ChocExpr

if TYPE_CHECKING:
    from .col import Col


@typechecked
class Window(ChocExpr):
    """
    Window function — FUNC(...) OVER (PARTITION BY ... ORDER BY ...)

    Use the static factory methods to build window expressions:
      Window.row_number(partition_by=[...], order_by=[...])
      Window.sum(Col("amount"), partition_by=[Col("dept")])
      Window.lag(Col("salary"), offset=1, order_by=[Col("hire_date")])
    """

    def __init__(
            self,
            func_str: str,
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> None:
        from .col import Col as ColClass
        self._func_str = func_str
        self._partition_by = [ColClass(c) if isinstance(c, str) else c for c in (partition_by or [])]
        self._order_by = [ColClass(c) if isinstance(c, str) else c for c in (order_by or [])]
        self._alias = alias
        super().__init__("{_window_expr}@{_alias}: AS {_alias}:;")

    @property
    def _over_clause(self) -> str:
        parts = []
        if self._partition_by:
            cols = ", ".join(c.full_name for c in self._partition_by)
            parts.append(f"PARTITION BY {cols}")
        if self._order_by:
            labels = ", ".join(c.ordering_label or c.full_name for c in self._order_by)
            parts.append(f"ORDER BY {labels}")
        return f"OVER ({' '.join(parts)})"

    @property
    def _window_expr(self) -> str:
        return f"{self._func_str} {self._over_clause}"

    def alias(self, name: str) -> Self:
        """ Set an alias """
        self._alias = name
        return self

    # ── No-argument window functions ────────────────────────────────────────

    @staticmethod
    def row_number(
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> Window:
        """ ROW_NUMBER() OVER (...) """
        return Window("ROW_NUMBER()", partition_by, order_by, alias)

    @staticmethod
    def rank(
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> Window:
        """ RANK() OVER (...) """
        return Window("RANK()", partition_by, order_by, alias)

    @staticmethod
    def dense_rank(
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> Window:
        """ DENSE_RANK() OVER (...) """
        return Window("DENSE_RANK()", partition_by, order_by, alias)

    @staticmethod
    def ntile(
            n: int,
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> Window:
        """ NTILE(n) OVER (...) """
        return Window(f"NTILE({n})", partition_by, order_by, alias)

    @staticmethod
    def cume_dist(
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> Window:
        """ CUME_DIST() OVER (...) """
        return Window("CUME_DIST()", partition_by, order_by, alias)

    @staticmethod
    def percent_rank(
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> Window:
        """ PERCENT_RANK() OVER (...) """
        return Window("PERCENT_RANK()", partition_by, order_by, alias)

    # ── Aggregate window functions ───────────────────────────────────────────

    @staticmethod
    def sum(
            col: Col | str,
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> Window:
        """ SUM(col) OVER (...) """
        from .col import Col as ColClass
        col = ColClass(col) if isinstance(col, str) else col
        return Window(f"SUM({col.full_name})", partition_by, order_by, alias)

    @staticmethod
    def avg(
            col: Col | str,
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> Window:
        """ AVG(col) OVER (...) """
        from .col import Col as ColClass
        col = ColClass(col) if isinstance(col, str) else col
        return Window(f"AVG({col.full_name})", partition_by, order_by, alias)

    @staticmethod
    def count(
            col: Col | str,
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> Window:
        """ COUNT(col) OVER (...) """
        from .col import Col as ColClass
        col = ColClass(col) if isinstance(col, str) else col
        return Window(f"COUNT({col.full_name})", partition_by, order_by, alias)

    @staticmethod
    def min(
            col: Col | str,
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> Window:
        """ MIN(col) OVER (...) """
        from .col import Col as ColClass
        col = ColClass(col) if isinstance(col, str) else col
        return Window(f"MIN({col.full_name})", partition_by, order_by, alias)

    @staticmethod
    def max(
            col: Col | str,
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> Window:
        """ MAX(col) OVER (...) """
        from .col import Col as ColClass
        col = ColClass(col) if isinstance(col, str) else col
        return Window(f"MAX({col.full_name})", partition_by, order_by, alias)

    # ── Value window functions ───────────────────────────────────────────────

    @staticmethod
    def lag(
            col: Col | str,
            offset: int = 1,
            default: int | float | str | None = None,
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> Window:
        """ LAG(col[, offset[, default]]) OVER (...) """
        from .col import Col as ColClass
        from ..utils import quote_expr
        col = ColClass(col) if isinstance(col, str) else col
        args = f"{col.full_name}, {offset}" + (f", {quote_expr(default)}" if default is not None else "")
        return Window(f"LAG({args})", partition_by, order_by, alias)

    @staticmethod
    def lead(
            col: Col | str,
            offset: int = 1,
            default: int | float | str | None = None,
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> Window:
        """ LEAD(col[, offset[, default]]) OVER (...) """
        from .col import Col as ColClass
        from ..utils import quote_expr
        col = ColClass(col) if isinstance(col, str) else col
        args = f"{col.full_name}, {offset}" + (f", {quote_expr(default)}" if default is not None else "")
        return Window(f"LEAD({args})", partition_by, order_by, alias)

    @staticmethod
    def first_value(
            col: Col | str,
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> Window:
        """ FIRST_VALUE(col) OVER (...) """
        from .col import Col as ColClass
        col = ColClass(col) if isinstance(col, str) else col
        return Window(f"FIRST_VALUE({col.full_name})", partition_by, order_by, alias)

    @staticmethod
    def last_value(
            col: Col | str,
            partition_by: Iterable[Col | str] | None = None,
            order_by: Iterable[Col | str] | None = None,
            alias: str | None = None
    ) -> Window:
        """ LAST_VALUE(col) OVER (...) """
        from .col import Col as ColClass
        col = ColClass(col) if isinstance(col, str) else col
        return Window(f"LAST_VALUE({col.full_name})", partition_by, order_by, alias)
