from enum import Enum


class JoinType(Enum):

    Inner = "INNER"
    Left = "LEFT"
    Right = "RIGHT"
    Full = "FULL"
    Cross = "CROSS"
    Natural = "NATURAL"
