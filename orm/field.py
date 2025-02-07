class Field():
    def __init__(self, name, field_type, primary_key=False, nullable=True, default=None):
        self.name = name
        self.field_type = field_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default

    # generates sql query for column definition
    def __str__(self):
        column_def = f"{self.name} {self.field_type}"
        if self.primary_key:
            column_def += " PRIMARY KEY"
        if not self.nullable:
            column_def += " NOT NULL"
        if self.default is not None:
            column_def += f" DEFAULT {repr(self.default)}"
        return column_def
