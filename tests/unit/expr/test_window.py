from chocolatine import Window, Col as _, Query


# ── No-arg functions ─────────────────────────────────────────────────────────

def test_row_number_partition_and_order():
    w = Window.row_number(partition_by=[_("dept")], order_by=[_("salary").desc()])
    assert w.build() == "ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC)"


def test_row_number_with_alias():
    w = Window.row_number(order_by=[_("salary").desc()]).alias("rn")
    assert w.build() == "ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn"


def test_row_number_alias_param():
    w = Window.row_number(order_by=[_("salary").desc()], alias="rn")
    assert w.build() == "ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn"


def test_rank():
    assert Window.rank(order_by=[_("salary").desc()]).build() == "RANK() OVER (ORDER BY salary DESC)"


def test_dense_rank():
    assert Window.dense_rank(order_by=[_("score").desc()]).build() == "DENSE_RANK() OVER (ORDER BY score DESC)"


def test_ntile():
    assert Window.ntile(4, order_by=[_("salary")]).build() == "NTILE(4) OVER (ORDER BY salary)"


def test_cume_dist():
    assert Window.cume_dist(order_by=[_("salary")]).build() == "CUME_DIST() OVER (ORDER BY salary)"


def test_percent_rank():
    assert Window.percent_rank(order_by=[_("salary")]).build() == "PERCENT_RANK() OVER (ORDER BY salary)"


def test_over_no_partition_no_order():
    assert Window.row_number().build() == "ROW_NUMBER() OVER ()"


# ── Aggregate window functions ───────────────────────────────────────────────

def test_sum_partition():
    assert Window.sum(_("amount"), partition_by=[_("dept")]).build() == "SUM(amount) OVER (PARTITION BY dept)"


def test_avg_partition_and_order():
    w = Window.avg(_("salary"), partition_by=[_("dept")], order_by=[_("hire_date")])
    assert w.build() == "AVG(salary) OVER (PARTITION BY dept ORDER BY hire_date)"


def test_count():
    assert Window.count(_("id"), partition_by=[_("dept")]).build() == "COUNT(id) OVER (PARTITION BY dept)"


def test_min():
    assert Window.min(_("salary"), partition_by=[_("dept")]).build() == "MIN(salary) OVER (PARTITION BY dept)"


def test_max():
    assert Window.max(_("salary"), partition_by=[_("dept")]).build() == "MAX(salary) OVER (PARTITION BY dept)"


def test_sum_with_str_col():
    assert Window.sum("amount", partition_by=["dept"]).build() == "SUM(amount) OVER (PARTITION BY dept)"


# ── Value window functions ───────────────────────────────────────────────────

def test_lag_default_offset():
    assert Window.lag(_("salary"), order_by=[_("hire_date")]).build() == "LAG(salary, 1) OVER (ORDER BY hire_date)"


def test_lag_custom_offset():
    assert Window.lag(_("salary"), offset=2, order_by=[_("hire_date")]).build() == "LAG(salary, 2) OVER (ORDER BY hire_date)"


def test_lag_with_default_value():
    assert Window.lag(_("salary"), offset=1, default=0, order_by=[_("hire_date")]).build() == "LAG(salary, 1, 0) OVER (ORDER BY hire_date)"


def test_lead():
    assert Window.lead(_("salary"), offset=1, order_by=[_("hire_date")]).build() == "LEAD(salary, 1) OVER (ORDER BY hire_date)"


def test_lead_with_default():
    assert Window.lead(_("salary"), offset=1, default="N/A", order_by=[_("hire_date")]).build() == "LEAD(salary, 1, 'N/A') OVER (ORDER BY hire_date)"


def test_first_value():
    w = Window.first_value(_("salary"), partition_by=[_("dept")], order_by=[_("hire_date")])
    assert w.build() == "FIRST_VALUE(salary) OVER (PARTITION BY dept ORDER BY hire_date)"


def test_last_value():
    w = Window.last_value(_("salary"), partition_by=[_("dept")], order_by=[_("hire_date")])
    assert w.build() == "LAST_VALUE(salary) OVER (PARTITION BY dept ORDER BY hire_date)"


# ── Integration with Query ───────────────────────────────────────────────────

def test_window_in_select():
    q = Query.get_rows("employees", cols=[
        _("name"),
        Window.row_number(partition_by=[_("dept")], order_by=[_("salary").desc()]).alias("rn"),
    ])
    assert q.build() == (
        "SELECT name, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn "
        "FROM employees"
    )
