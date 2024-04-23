from enum import Enum


class SqlFunction(Enum):

    Upper = "UPPER"
    Lower = "LOWER"
    Left = "LEFT"
    Right = "RIGHT"
    Length = "LENGTH"
    Abs = "ABS"
    Round = "ROUND"
    Ceiling = "CEILING"
    Floor = "FLOOR"
    Second = "SECOND"
    Minute = "MINUTE"
    Hour = "HOUR"
    Day = "DAY"
    Month = "MONTH"
    Year = "YEAR"
    Now = "NOW"
    Date = "DATE"
    DateDiff = "DATEDIFF"
    Coalesce = "COALESCE"
