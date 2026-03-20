from enum import Enum

class SqlType(Enum):

    Integer = "INT"
    TinyInteger = "TINYINT"
    SmallInteger = "SMALLINT"
    BigInteger = "BIGINT"
    Float = "FLOAT"
    Double = "DOUBLE"
    Decimal = "DECIMAL"
    String = "VARCHAR(255)"
    Char = "CHAR"
    Text = "TEXT"
    Boolean = "BOOLEAN"
    Date = "DATE"
    DateTime = "DATETIME"
    Timestamp = "TIMESTAMP"
    Json = "JSON"
    Blob = "BLOB"
