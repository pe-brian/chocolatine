from chocolatine import Table


def test_table_init():
    assert Table(name="name", alias="alias", schema="schema").build() == "schema.name AS alias"
    assert Table(name="name", schema="schema").build() == "schema.name"
    assert Table(name="name").build() == "name"
    assert Table(name="name", alias="alias").build() == "name AS alias"


def test_table_init_with_name_as_only_argument():
    assert Table(name="schema.name@alias").build() == "schema.name AS alias"
    assert Table(name="schema.name:alias").build() == "schema.name AS alias"
    assert Table(name="schema.name").build() == "schema.name"
    assert Table(name="name").build() == "name"
    assert Table(name="name@alias").build() == "name AS alias"
    assert Table(name="name:alias").build() == "name AS alias"


def test_table_set_alias():
    table = Table(name="schema.name")
    table.alias("alias")
    assert table.build() == "schema.name AS alias"


def test_table_full_name():
    assert Table(name="schema.name@alias").full_name == "schema.name"
