import pytest
from chocolatine import Query, Col as _, QueryMode


def test_query_expected_errors():
    with pytest.raises(ValueError):
        Query(assignations=(_("col") == "pain au chocolat",))

    with pytest.raises(ValueError):
        Query(query_mode=QueryMode.Update, cols=("col_A", "col_B"))
