from chocolatine import now, curdate, Col as _


def test_now():
    assert now().build() == "NOW()"


def test_curdate():
    assert curdate().build() == "CURDATE()"


def test_now_in_condition():
    assert (_("updated_at") == now()).build() == "(updated_at = NOW())"


def test_curdate_in_condition():
    assert (_("created_at") > curdate()).build() == "(created_at > CURDATE())"


def test_now_with_alias():
    assert now().alias("ts").build() == "NOW() AS ts"
