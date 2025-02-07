from .base_model import BaseModel


class Collection(BaseModel):
    table_name = 'collections'

    def __init__(self):
        super().__init__()
        self.add_field(**{'name': 'id', 'field_type': 'INT AUTO_INCREMENT',
                          'primary_key': True, 'nullable': False})
        self.add_field(
            **{'name': 'collection', 'field_type': 'VARCHAR(255)', 'nullable': True})
        self.add_field(
            **{'name': 'name', 'field_type': 'VARCHAR(255)', 'nullable': True})
        self.add_field(
            **{'name': 'description', 'field_type': 'TEXT', 'nullable': True})
        self.add_field(**{'name': 'image_url',
                          'field_type': 'VARCHAR(255)', 'nullable': True})
        self.add_field(
            **{'name': 'owner', 'field_type': 'VARCHAR(255)', 'nullable': True})
        self.add_field(**{'name': 'twitter_username',
                          'field_type': 'VARCHAR(255)', 'nullable': True})
        self.add_field(
            **{'name': 'contracts', 'field_type': 'JSON', 'nullable': True})
