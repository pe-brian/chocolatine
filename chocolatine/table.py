class Table:

    def __init__(self, name: str, new_name: str = None):
        self.name = name
        self.new_name = new_name

    def alias(self, new_name: str):
        self.new_name = new_name
        return self

    def build(self):
        expr = self.name
        if self.new_name:
            expr += f" AS {self.new_name}"
        return expr

    def __str__(self):
        return self.build()

    def __expr__(self):
        return self.build()
