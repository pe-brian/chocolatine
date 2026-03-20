from chocolatine import Limit


def test_limit():
    assert Limit(length=1).build() == "LIMIT 1"


def test_limit_zero_raises():
    import pytest
    with pytest.raises(ValueError):
        Limit(length=0)


def test_limit_negative_raises():
    import pytest
    with pytest.raises(ValueError):
        Limit(length=-1)
