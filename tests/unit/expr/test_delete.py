from chocolatine import Delete


def test_delete_build():
    assert Delete().build() == "DELETE"
