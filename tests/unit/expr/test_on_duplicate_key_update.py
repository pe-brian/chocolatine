from chocolatine import Query, Col as _


def test_insert_unchanged_without_on_duplicate():
    q = Query.insert_row("users", [_("id"), _("name")], (1, "John"))
    assert q.build() == "INSERT INTO users (id, name) VALUES (1, 'John')"


def test_on_duplicate_single_assignation():
    q = Query.insert_row("users", [_("id"), _("name"), _("email")], (1, "John", "john@example.com"))
    q.on_duplicate_key_update(_("name") == "John")
    assert q.build() == "INSERT INTO users (id, name, email) VALUES (1, 'John', 'john@example.com') ON DUPLICATE KEY UPDATE (name = 'John')"


def test_on_duplicate_multiple_assignations():
    q = Query.insert_row("users", [_("id"), _("name"), _("email")], (1, "John", "john@example.com"))
    q.on_duplicate_key_update(_("name") == "John", _("email") == "john@example.com")
    assert q.build() == "INSERT INTO users (id, name, email) VALUES (1, 'John', 'john@example.com') ON DUPLICATE KEY UPDATE (name = 'John'), (email = 'john@example.com')"


def test_on_duplicate_col_to_col():
    q = Query.insert_row("users", [_("id"), _("score")], (1, 42))
    q.on_duplicate_key_update(_("score") == _("score"))
    assert q.build() == "INSERT INTO users (id, score) VALUES (1, 42) ON DUPLICATE KEY UPDATE (score = score)"


def test_on_duplicate_with_insert_rows():
    q = Query.insert_rows("users", [_("id"), _("name")], [(1, "Alice"), (2, "Bob")])
    q.on_duplicate_key_update(_("name") == _("name"))
    assert q.build() == "INSERT INTO users (id, name) VALUES (1, 'Alice'), (2, 'Bob') ON DUPLICATE KEY UPDATE (name = name)"


def test_on_duplicate_fluent_chain():
    q = (
        Query.insert_row("users", [_("id"), _("name")], (1, "John"))
        .on_duplicate_key_update(_("name") == "John")
    )
    assert q.build() == "INSERT INTO users (id, name) VALUES (1, 'John') ON DUPLICATE KEY UPDATE (name = 'John')"
