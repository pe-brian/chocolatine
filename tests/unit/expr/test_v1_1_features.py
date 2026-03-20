"""Tests for v1.1.0 features."""
import pytest
from chocolatine import Query, Col as _, SqlType, JoinType
from chocolatine.expr.foreign_key import ForeignKey


# --- CHECK constraint ---

def test_col_check_constraint():
    col = _("price", type=SqlType.Float, check="price > 0")
    assert "CHECK (price > 0)" in col.creation_name


def test_col_check_with_not_null():
    col = _("age", type=SqlType.Integer, not_null=True, check="age >= 0")
    cn = col.creation_name
    assert "NOT NULL" in cn
    assert "CHECK (age >= 0)" in cn


def test_col_no_check_by_default():
    col = _("price", type=SqlType.Float)
    assert "CHECK" not in col.creation_name


# --- FOREIGN KEY ---

def test_foreign_key_basic():
    fk = ForeignKey("customer_id", references="customers")
    assert fk.creation_name == "FOREIGN KEY (customer_id) REFERENCES customers(id)"


def test_foreign_key_custom_ref_col():
    fk = ForeignKey("user_id", references="users", ref_col="uid")
    assert "REFERENCES users(uid)" in fk.creation_name


def test_foreign_key_on_delete():
    fk = ForeignKey("customer_id", references="customers", on_delete="CASCADE")
    assert "ON DELETE CASCADE" in fk.creation_name


def test_foreign_key_on_update():
    fk = ForeignKey("customer_id", references="customers", on_update="SET NULL")
    assert "ON UPDATE SET NULL" in fk.creation_name


def test_foreign_key_in_create_table():
    q = Query.create_table("orders", cols=[
        _("id", type=SqlType.Integer),
        _("customer_id", type=SqlType.Integer),
        ForeignKey("customer_id", references="customers", on_delete="CASCADE"),
    ])
    sql = q.build()
    assert "FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE" in sql


# --- LIMIT in UPDATE/DELETE ---

def test_update_with_limit():
    q = Query.update_rows("users", filters=[_("active") == 0], assignations=[_("active") == 1])
    q.head(10)
    assert q.build().endswith("LIMIT 10")


def test_delete_with_limit():
    q = Query.delete_rows("logs", filter=_("old") == 1)
    q.head(100)
    assert q.build().endswith("LIMIT 100")


# --- Explicit ORDER BY ---

def test_order_by_explicit():
    q = Query.get_rows("users")
    q.order_by(_("name").asc())
    assert "ORDER BY name ASC" in q.build()


def test_order_by_explicit_desc():
    q = Query.get_rows("users")
    q.order_by(_("created_at").desc())
    assert "ORDER BY created_at DESC" in q.build()


def test_order_by_multiple_cols():
    q = Query.get_rows("users")
    q.order_by(_("last_name").asc(), _("first_name").asc())
    assert "ORDER BY last_name ASC, first_name ASC" in q.build()


def test_order_by_string_defaults_asc():
    q = Query.get_rows("users")
    q.order_by("name")
    assert "ORDER BY name ASC" in q.build()


def test_order_by_col_not_in_select():
    q = Query.get_rows("users", cols=[_("name")])
    q.order_by(_("created_at").desc())
    built = q.build()
    assert "ORDER BY created_at DESC" in built
    assert "created_at AS" not in built  # not aliased in SELECT


# --- GROUP BY with Col ---

def test_group_by_with_col():
    q = Query.get_rows("orders")
    q.group_by(_("customer_id"))
    assert "GROUP BY customer_id" in q.build()


def test_group_by_mixed():
    q = Query.get_rows("orders")
    q.group_by("customer_id", _("status"))
    assert "GROUP BY customer_id, status" in q.build()


# --- INSERT INTO ... SELECT ... ---

def test_insert_select_no_cols():
    src = Query.get_rows("temp_users")
    q = Query.insert_select("users", src)
    assert q.build() == "INSERT INTO users SELECT * FROM temp_users"


def test_insert_select_with_cols():
    src = Query.get_rows("temp_users", cols=[_("name"), _("email")])
    q = Query.insert_select("users", src, cols=[_("name"), _("email")])
    built = q.build()
    assert "INSERT INTO users (name, email)" in built
    assert "SELECT name, email FROM temp_users" in built


def test_insert_select_with_filter():
    src = Query.get_rows("temp_users", filters=[_("active") == 1])
    q = Query.insert_select("users", src)
    assert "WHERE (active = 1)" in q.build()


# --- CREATE INDEX ---

def test_create_index_basic():
    q = Query.create_index("idx_email", "users", [_("email")])
    assert q.build() == "CREATE INDEX idx_email ON users (email)"


def test_create_unique_index():
    q = Query.create_index("idx_email", "users", [_("email")], unique=True)
    assert q.build() == "CREATE UNIQUE INDEX idx_email ON users (email)"


def test_create_index_multiple_cols():
    q = Query.create_index("idx_name", "users", [_("last_name"), _("first_name")])
    assert q.build() == "CREATE INDEX idx_name ON users (last_name, first_name)"


# --- Parameterized queries ---

def test_build_parameterized_basic():
    q = Query.get_rows("users", filters=[_("name") == "Alice"])
    sql, params = q.build_parameterized()
    assert sql == "SELECT * FROM users WHERE (name = %s)"
    assert params == ("Alice",)


def test_build_parameterized_multiple():
    q = Query.get_rows("users", filters=[(_("age") > 18) & (_("city") == "Paris")])
    sql, params = q.build_parameterized()
    assert "%s" in sql
    assert 18 in params
    assert "Paris" in params


def test_build_parameterized_insert():
    q = Query.insert_row("users", [_("name"), _("email")], ("Alice", "alice@example.com"))
    sql, params = q.build_parameterized()
    assert sql == "INSERT INTO users (name, email) VALUES (%s, %s)"
    assert params == ("Alice", "alice@example.com")


def test_build_parameterized_does_not_affect_normal_build():
    q = Query.get_rows("users", filters=[_("name") == "Alice"])
    q.build_parameterized()
    # Normal build still works with literal values
    assert q.build() == "SELECT * FROM users WHERE (name = 'Alice')"


def test_build_parameterized_update():
    q = Query.update_rows("users", filters=[_("id") == 1], assignations=[_("name") == "Bob"])
    sql, params = q.build_parameterized()
    assert sql == "UPDATE users SET (name = %s) WHERE (id = %s)"
    assert set(params) == {"Bob", 1}


# --- View ---

def test_view_create():
    from chocolatine.expr.view import View
    from chocolatine.enums.view_mode import ViewMode
    q = Query.get_rows("users", filters=[_("active") == 1])
    v = View("active_users", query=q)
    assert v.build() == "CREATE VIEW active_users AS SELECT * FROM users WHERE (active = 1)"


def test_view_drop():
    from chocolatine.expr.view import View
    from chocolatine.enums.view_mode import ViewMode
    v = View("active_users", mode=ViewMode.Drop)
    assert v.build() == "DROP VIEW active_users"
