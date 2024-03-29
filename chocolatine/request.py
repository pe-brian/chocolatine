from .condition import Condition
from .col import Col


class Request:

    def __init__(self, compact: bool = True):
        self.table_name = None
        self.selected_cols = []
        self.unique = False
        self.group_by_cols = []
        self.where_condition = []
        self.having_condition = []
        self.compact = compact

    def table(self, table_name: str):
        self.table_name = table_name
        return self

    def select(self, *cols):
        self.cols = cols
        return self

    def distinct(self):
        self.unique = True
        return self

    def filter(self, where_condition: Condition = None, having_condition: Condition = None):
        if where_condition is None and having_condition is None:
            raise Exception("At least one of where or having condition must be specified")
        self.where_condition = where_condition
        self.having_condition = having_condition
        return self

    def group_by(self, *cols):
        self.group_by_cols = cols
        return self

    def build_select(self):
        expr = "SELECT "
        cols = ", ".join([str(col) for col in self.cols])
        if self.unique:
            expr += f"DISTINCT({cols})"
        else:
            expr += cols
        return expr

    def build_from(self):
        return f"FROM {self.table_name}"

    def build_where(self):
        if self.where_condition:
            return f"WHERE {self.where_condition}"
        return ""

    def build_group_by(self):
        if self.group_by_cols:
            return f"GROUP BY {", ".join(self.group_by_cols)}"
        return ""

    def build_having(self):
        if self.having_condition:
            return f"HAVING {self.having_condition}"
        return ""

    def build_order_by(self):
        ordering = []
        for col in self.cols:
            if type(col) is Col and col.ordering is not None:
                ordering.append(f"{col.name} {col.ordering.value}")
        if ordering:
            return f"ORDER BY {", ".join(ordering)}"
        return ""

    def build(self):
        return f"{" " if self.compact else "\n"}".join(
            part for part in [
                self.build_select(),
                self.build_from(),
                self.build_where(),
                self.build_group_by(),
                self.build_having(),
                self.build_order_by()
            ] if part
        )

    def __str__(self):
        return self.build()

    def __expr__(self):
        return self.build()
