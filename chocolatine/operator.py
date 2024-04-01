from enum import Enum


class Operator(Enum):

    LowerThan = "<"
    GreaterThan = ">"
    LowerOrEqualThan = "<="
    GreaterOrEqualThan = ">="
    Equal = "="
    NotEqual = "<>"
    And = "AND"
    Or = "OR"
    Like = "LIKE"
    In = "IN"
