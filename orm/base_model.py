from .field import Field


class BaseModel():
    # specified in subclass
    table_name = None

    def __init__(self):
        self.fields = []

    # add field to the model
    def add_field(self, **field):
        if isinstance(field, dict):
            self.fields.append(Field(**field))
        else:
            raise ValueError(
                "Each field should be provided as a dictionary")

    # generates sql query
    def __str__(self):
        if not self.table_name:
            raise ValueError("Table name must be specified in the subclass")

        if not self.fields:
            raise ValueError("At least one field should be added")

        fields_str = ", ".join([str(field) for field in self.fields])
        return f"CREATE TABLE IF NOT EXISTS {self.table_name} ({fields_str});"
