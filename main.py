from database_manager import DatabaseManager
from data_manager import DataManager
from models import Collection
import os
import json
from dotenv import load_dotenv
load_dotenv()


def main():
    api_key = os.getenv('OPENSEA_API_KEY')
    base_url = 'https://api.opensea.io/api/v2/collections'
    headers = {'accept': 'application/json', 'X-API-KEY': api_key}
    limit = 10
    chain = 'ethereum'
    next_page = ''

    #  define data manager class that handles etl processes
    data_manager = DataManager(
        base_url=base_url, headers=headers, limit=limit, chain=chain, next_page=next_page)

    extracted_data = data_manager.extract_data()
    data_manager.save_raw_data(filename='ethereum', data=extracted_data)
    loaded_raw_data = data_manager.load_raw_data()
    print('Json raw data. last version : ', loaded_raw_data['json_raw_data'])
    print('Csv raw data. last version : ', loaded_raw_data['csv_raw_data'])

    transformed_data = data_manager.transform_data(data=extracted_data)

    # database connection
    db_manager = DatabaseManager(
        host=os.getenv('DATABASE_HOST'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD')
    )
    db_manager.connect()
    db_manager.exists_or_create_db(database_name='ethereum')
    db_manager.use_db()

    #  create collection model and create corresponding table in the db
    collection = Collection()
    db_manager.create_table(collection)

    db_manager.insert_many(table_name='collections',
                           data_list=transformed_data)

    eth_collections = db_manager.select()
    print(eth_collections)


if __name__ == '__main__':
    main()
