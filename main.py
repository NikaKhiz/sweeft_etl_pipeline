from orm.database_manager import DatabaseManager
from data_manager import DataManager
from orm.models import Collection
import os
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

    # select statements
    select_limited = db_manager.select_limited()
    # print(select_limited)
    select_ordered_by_desc = db_manager.select_ordered_by_desc(
        order_by='id', limit=20)
    # print(select_ordered_by_desc)
    select_ordered_by_asc = db_manager.select_ordered_by_asc(
        order_by='id', limit=20)
    # print(select_ordered_by_asc)
    select_like = db_manager.select_like(column='name',
                                         like='IGNATIUS')
    # print(select_like)
    select_ilike = db_manager.select_ilike(column='name',
                                           like='mArIlyn')
    # print(select_ilike)
    select_in = db_manager.select_in(column='id',
                                     col_in='1,13,15')
    # print(select_in)


if __name__ == '__main__':
    main()
