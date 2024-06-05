from enum import Enum


class QueryMode(Enum):

    Select = "SELECT"
    Update = "UPDATE"
    Delete = "DELETE"
    Create = "CREATE"
    Alter = "ALTER"
