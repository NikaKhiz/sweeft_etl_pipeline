import mysql.connector
import json


class DatabaseManager():
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, conn):
        self._conn = conn

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, cursor):
        self._cursor = cursor

    @classmethod
    def connect(cls, host, user, password):
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )
        cursor = conn.cursor()

        return cls(conn, cursor)

    # create database with given name if not exists
    def exists_or_create_db(self, database_name='ethereum'):
        self.cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in self.cursor.fetchall()]
        if database_name not in databases:
            self.cursor.execute(f"CREATE DATABASE {database_name}")

    # use database of given name
    def use_db(self, database_name='ethereum'):
        self.cursor.execute(f"USE {database_name}")

    # create table of collections if not exists
    def exists_or_create_table(self, table_name='collections'):
        self.cursor.execute("SHOW TABLES")
        tables = [table[0] for table in self.cursor.fetchall()]

        if table_name not in tables:
            self.cursor.execute(f"""
                                    CREATE TABLE {table_name } (
                                        id INT AUTO_INCREMENT PRIMARY KEY,
                                        collection VARCHAR(255),
                                        name VARCHAR(255),
                                        description TEXT,
                                        image_url VARCHAR(255),
                                        owner VARCHAR(255),
                                        twitter_username VARCHAR(255),
                                        contracts JSON
                                        )
                                    """
                                )

    # insert data in to the collections table
    def insert_collections(self, data):
        sql = """INSERT INTO collections (collection, name, description, image_url, owner, twitter_username, contracts)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        for item in data:
            values = (item['collection'], item['name'], item['description'], item['image_url'],
                      item['owner'], item['twitter_username'], json.dumps(item['contracts']))
            self.cursor.execute(sql, values)
            self.conn.commit()
