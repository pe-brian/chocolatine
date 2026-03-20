from chocolatine import Col as _, Query, Window, Coalesce


# ── Basic operations ─────────────────────────────────────────────────────────

def test_mul():
    assert (_("qty") * _("unit_price")).build() == "(qty * unit_price)"


def test_add():
    assert (_("price") + _("tax")).build() == "(price + tax)"


def test_sub():
    assert (_("revenue") - _("cost")).build() == "(revenue - cost)"


def test_div():
    assert (_("total") / _("count")).build() == "(total / count)"


def test_mod():
    assert (_("value") % 10).build() == "(value % 10)"


# ── Scalars ──────────────────────────────────────────────────────────────────

def test_mul_scalar_int():
    assert (_("price") * 2).build() == "(price * 2)"


def test_mul_scalar_float():
    assert (_("price") * 1.2).build() == "(price * 1.2)"


def test_add_scalar():
    assert (_("stock") + 1).build() == "(stock + 1)"


# ── Reflected operators ──────────────────────────────────────────────────────

def test_rmul():
    assert (2 * _("price")).build() == "(2 * price)"


def test_radd():
    assert (10 + _("bonus")).build() == "(10 + bonus)"


def test_rsub():
    assert (100 - _("discount")).build() == "(100 - discount)"


def test_rdiv():
    assert (1 / _("rate")).build() == "(1 / rate)"


# ── Chaining ─────────────────────────────────────────────────────────────────

def test_chained():
    expr = (_("qty") * _("unit_price")) - _("discount")
    assert expr.build() == "((qty * unit_price) - discount)"


def test_chained_with_scalar():
    expr = _("revenue") / _("sessions") * 100
    assert expr.build() == "((revenue / sessions) * 100)"


# ── Alias ────────────────────────────────────────────────────────────────────

def test_alias():
    assert (_("qty") * _("unit_price")).alias("total").build() == "(qty * unit_price) AS total"


def test_alias_chained():
    assert ((_("qty") * _("unit_price")) - _("discount")).alias("net").build() == "((qty * unit_price) - discount) AS net"


# ── Comparisons (produce Condition) ─────────────────────────────────────────

def test_gt():
    assert (_("qty") * _("price") > 100).build() == "((qty * price) > 100)"


def test_lt():
    assert (_("revenue") - _("cost") < 0).build() == "((revenue - cost) < 0)"


def test_eq():
    assert (_("a") + _("b") == 10).build() == "((a + b) = 10)"


def test_ge():
    assert (_("score") * 2 >= 100).build() == "((score * 2) >= 100)"


def test_le():
    assert (_("price") / 2 <= 50).build() == "((price / 2) <= 50)"


def test_ne():
    assert (_("a") + _("b") != 0).build() == "((a + b) <> 0)"


# ── Integration ──────────────────────────────────────────────────────────────

def test_in_select():
    q = Query.get_rows("order_items", cols=[
        _("product_id"),
        (_("qty") * _("unit_price")).alias("total"),
    ])
    assert q.build() == "SELECT product_id, (qty * unit_price) AS total FROM order_items"


def test_in_filter():
    q = Query.get_rows("order_items", filters=[_("qty") * _("unit_price") > 500])
    assert q.build() == "SELECT * FROM order_items WHERE ((qty * unit_price) > 500)"


def test_in_window():
    w = Window.sum(_("qty") * _("unit_price"), partition_by=[_("customer_id")]).alias("total")
    assert w.build() == "SUM((qty * unit_price)) OVER (PARTITION BY customer_id) AS total"


def test_in_coalesce():
    expr = Coalesce(_("discount") * _("price"), 0).alias("rebate")
    assert expr.build() == "COALESCE((discount * price), 0) AS rebate"
