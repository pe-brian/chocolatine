from chocolatine import Assignation, Col as _


def test_assignation_scalar():
    assert Assignation(_('col'), 1).build() == 'col = 1'
    assert Assignation('col', 1).build() == 'col = 1'


def test_assignation_col():
    assert Assignation(_('col_A'), _('col_B')).build() == 'col_A = col_B'
    assert Assignation('col_A', 'col_B').build() == 'col_A = col_B'
