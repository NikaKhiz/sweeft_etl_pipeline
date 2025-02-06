from database_manager import DatabaseManager
from data_manager import DataManager
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

    data_manager = DataManager(
        base_url=base_url, headers=headers, limit=limit, chain=chain)

    extracted_data = data_manager.extract_data()
    data_manager.save_raw_data(filename='ethereum', data=extracted_data)
    loaded_raw_data = data_manager.load_raw_data()
    print('Json raw data. last version : ', loaded_raw_data['json_raw_data'])
    print('Csv raw data. last version : ', loaded_raw_data['csv_raw_data'])

    transformed_data = data_manager.transform_data(data=extracted_data)
    print('Transformed data : ', json.dumps(transformed_data, indent=2))

    database_manager = DatabaseManager.connect(
        host=os.getenv('DATABASE_HOST'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD')
    )

    database_manager.exists_or_create_db(database_name='ethereum')
    database_manager.use_db(database_name='ethereum')
    database_manager.exists_or_create_table(table_name='collections')
    database_manager.insert_collections(data=transformed_data)


if __name__ == '__main__':
    main()
