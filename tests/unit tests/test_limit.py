from chocolatine import Limit


def test_limit():
    assert Limit(length=1).build() == "LIMIT 1"
