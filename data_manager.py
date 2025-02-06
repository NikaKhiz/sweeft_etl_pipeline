import requests
import json
from file_manager import FileManager


class DataManager():
    def __init__(self, base_url, headers, limit, chain):
        self.base_url = base_url
        self.headers = headers
        self.limit = limit
        self.chain = chain
        self.file_manager = FileManager()

    # extracts data from opensea api
    def extract_data(self):
        response = requests.get(
            f'{self.base_url}?chain={self.chain}&limit={self.limit}', headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Failed to extract data: {response.status_code}')

    # prepare data for database insertion
    def transform_data(self, data):
        transformed_data = []
        for collection in data.get('collections', []):
            transformed_data.append({
                'collection': collection.get('collection'),
                'name': collection.get('name'),
                'description': collection.get('description'),
                'image_url': collection.get('image_url'),
                'owner': collection.get('owner'),
                'twitter_username': collection.get('twitter_username'),
                'contracts': collection.get('contracts'),
            })
        return transformed_data

    # save raw data into csv and json formats
    def save_raw_data(self, data, filename):
        self.file_manager.json_writer(filename=filename, data=data)
        self.file_manager.csv_writer(filename=filename, data=data)

    # loads data from local data lake. recent one if no filename provided.
    def load_raw_data(self, filename=None):
        json_data = self.file_manager.json_reader(filename=filename)
        csv_data = self.file_manager.csv_reader(filename=filename)
        return {
            'json_raw_data': json_data,
            'csv_raw_data': csv_data
        }
