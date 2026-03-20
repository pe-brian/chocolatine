import pytest
from chocolatine import Coalesce, Col as _, Query


def test_coalesce_cols():
    assert Coalesce(_("first_name"), _("last_name")).build() == "COALESCE(first_name, last_name)"


def test_coalesce_col_and_literal_str():
    assert Coalesce(_("email"), "no-email").build() == "COALESCE(email, 'no-email')"


def test_coalesce_col_and_literal_int():
    assert Coalesce(_("amount"), 0).build() == "COALESCE(amount, 0)"


def test_coalesce_three_args():
    assert Coalesce(_("first_name"), _("last_name"), "unknown").build() == "COALESCE(first_name, last_name, 'unknown')"


def test_coalesce_with_null():
    assert Coalesce(None, _("fallback"), "default").build() == "COALESCE(NULL, fallback, 'default')"


def test_coalesce_with_alias_param():
    assert Coalesce(_("email"), "no-email", alias="contact").build() == "COALESCE(email, 'no-email') AS contact"


def test_coalesce_with_alias_fluent():
    assert Coalesce(_("email"), "no-email").alias("contact").build() == "COALESCE(email, 'no-email') AS contact"


def test_coalesce_table_prefixed_col():
    assert Coalesce(_("u.email"), _("p.email"), "none").build() == "COALESCE(u.email, p.email, 'none')"


def test_coalesce_too_few_args_raises():
    with pytest.raises(ValueError):
        Coalesce(_("email"))


def test_coalesce_in_select():
    q = Query.get_rows(table="users", cols=[Coalesce(_("first_name"), "anonymous").alias("name")])
    assert q.build() == "SELECT COALESCE(first_name, 'anonymous') AS name FROM users"
