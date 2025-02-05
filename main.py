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

    collections = json.dumps(response.json()['collections'], indent=2)

    print(collections)


if __name__ == '__main__':
    main()
