from chocolatine import ChocExprAttr


def test_choc_expr_attr():

    class C:
        def __init__(self) -> None:
            self.val = 42

    class B:
        def __init__(self) -> None:
            self.c = C()

    class A:
        def __init__(self) -> None:
            self.b = B()

    class Box:
        def __init__(self) -> None:
            self.items = (A(), A(), A())

    class MainBox:
        def __init__(self) -> None:
            self.box = Box()
            self.items = (1, 2, 3)
            self.val = 1

    box = Box()
    main_box = MainBox()

    assert ChocExprAttr(main_box, "val").build() == "1"
    assert ChocExprAttr(main_box, "$(items)").build() == "1, 2, 3"
    assert ChocExprAttr(box, "$(items).b.c.val").build() == "42, 42, 42"
    assert ChocExprAttr(box, "$(items).b.c.val").build() == "42, 42, 42"
    assert ChocExprAttr(main_box, "$(box.items).b.c.val").build() == "42, 42, 42"
