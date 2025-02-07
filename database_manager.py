import mysql.connector
import json


class DatabaseManager():
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.conn = None
        self.cursor = None

    # connects to the db
    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
        )

        self.cursor = self.conn.cursor()

    # closes connection
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    # creates database with given name if not exists
    def exists_or_create_db(self, database_name='ethereum'):
        db_show_query = f'SHOW DATABASES'
        dbs = self.fetch_all(db_show_query)
        databases = [db[0] for db in dbs]

        if database_name not in databases:
            db_create_query = f"CREATE DATABASE {database_name}"
            self.execute(db_create_query)

    # uses database of given name
    def use_db(self, database_name='ethereum'):
        query = f"USE {database_name}"
        self.execute(query)

    # executes the given query
    def execute(self, query, values=None):
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        self.conn.commit()

        # executes the given query
    def executemany(self, query, values=None):
        if values:
            self.cursor.executemany(query, values)
        else:
            self.cursor.executemany(query)
        self.conn.commit()

    # fetches results of query from cursor
    def fetch_all(self, query, values=None):
        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    # creates db table
    def create_table(self, table_model):
        query = str(table_model)
        self.execute(query)

    # drops db table
    def drop_table(self, table_name):
        query = f"DROP TABLE IF EXISTS {table_name};"
        self.execute(query)

    # adds a new column to a table
    def add_column(self, table_name, definition):
        query = f"ALTER TABLE {table_name} ADD COLUMN {definition};"
        try:
            self.execute(query)
        except mysql.connector.errors.ProgrammingError:
            print('column with given name already exists')

    # removes column from a table

    def remove_column(self, table_name, column_name):
        query = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"
        try:
            self.execute(query)
        except mysql.connector.errors.ProgrammingError:
            print('column with given name doesnt exists')

    # modifies existing column
    def modify_column(self, table_name, column_name, data_type):
        query = f"ALTER TABLE {table_name} MODIFY COLUMN {column_name} {data_type};"
        try:
            self.execute(query)
        except mysql.connector.errors.ProgrammingError:
            print('no such column')

    # insert query
    def insert(self, table_name='collections', data=None):
        if not data:
            raise ValueError("No data provided for insertion")

        columns = ', '.join(data.keys())
        values = []

        for value in data.values():
            # if the value is a list or dictionary serialize it as json string
            if isinstance(value, (list, dict)):
                values.append(json.dumps(value))
            else:
                values.append(value)

        # Prepare the SQL query to insert the data
        values_placeholder = ', '.join(['%s' for _ in data.values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholder});"

        self.execute(query, tuple(values))

    def insert_many(self, table_name, data_list=[]):
        if not data_list:
            raise ValueError("No data provided for insertion")

        columns = ', '.join(data_list[0].keys())
        values_placeholder = ', '.join(['%s' for _ in data_list[0].keys()])

        # Prepare the list of values for all rows
        values_list = []
        for data in data_list:
            row_values = []
            for value in data.values():
                # if the value is a list or dictionary serialize it as json string
                if isinstance(value, (list, dict)):
                    row_values.append(json.dumps(value))
                else:
                    row_values.append(value)
            values_list.append(tuple(row_values))

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholder})"
        self.executemany(query, values_list)

    # select query
    def select(self, columns='*', where=None, table_name='collections'):
        query = f"SELECT {columns} FROM {table_name}"
        if where:
            query += f" WHERE {where}"

        rows = self.fetch_all(query)
        column_names = [desc[0] for desc in self.cursor.description]
        result = []
        for row in rows:
            row_dict = dict(zip(column_names, row))
            result.append(row_dict)

        return json.dumps(result, indent=2)
