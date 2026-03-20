from enum import Enum


class QueryMode(Enum):

    Select = "SELECT"
    Update = "UPDATE"
    Delete = "DELETE"
    Create = "CREATE"
    Alter = "ALTER"
    Insert = "INSERT"
    Drop = "DROP"
    Truncate = "TRUNCATE"
    InsertSelect = "INSERT_SELECT"
    CreateIndex = "CREATE_INDEX"
