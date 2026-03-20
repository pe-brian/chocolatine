from __future__ import annotations

from typing import Literal

from typeguard import typechecked

FKAction = Literal["CASCADE", "SET NULL", "SET DEFAULT", "RESTRICT", "NO ACTION"]


@typechecked
class ForeignKey:
    """
    Foreign key constraint for use in CREATE TABLE.

    Example:
        Query.create_table("orders", cols=[
            Col("id", type=SqlType.Integer),
            Col("customer_id", type=SqlType.Integer),
            ForeignKey("customer_id", references="customers", ref_col="id", on_delete="CASCADE"),
        ], auto_id=True)
        # ... FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
    """

    def __init__(
            self,
            col: str,
            references: str,
            ref_col: str = "id",
            on_delete: FKAction | None = None,
            on_update: FKAction | None = None
    ) -> None:
        self._col = col
        self._references = references
        self._ref_col = ref_col
        self._on_delete = on_delete
        self._on_update = on_update

    @property
    def creation_name(self) -> str:
        sql = f"FOREIGN KEY ({self._col}) REFERENCES {self._references}({self._ref_col})"
        if self._on_delete:
            sql += f" ON DELETE {self._on_delete}"
        if self._on_update:
            sql += f" ON UPDATE {self._on_update}"
        return sql
