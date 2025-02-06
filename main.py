from database_manager import DatabaseManager
from file_manager import FileManager
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()


def main():
    api_key = os.getenv('OPENSEA_API_KEY')

    base_url = "https://api.opensea.io/api/v2/collections?chain=ethereum&limit=3"
    headers = {"accept": "application/json", 'X-API-KEY': api_key}
    response = requests.get(base_url, headers=headers)

    file_manager = FileManager()
    file_manager.json_writer(filename='ethereum_json', data=response.json())
    file_manager.csv_writer(filename='ethereum_csv', data=response.json())
    print(file_manager.json_reader())
    print(file_manager.csv_reader())

    database_manager = DatabaseManager.connect(
        host=os.getenv('DATABASE_HOST'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD')
    )

    database_manager.exists_or_create_db(database_name='ethereum')
    database_manager.use_db(database_name='ethereum')
    database_manager.exists_or_create_table(table_name='collections')


if __name__ == '__main__':
    main()
