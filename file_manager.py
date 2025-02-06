import os
import json
import csv
from datetime import datetime


class FileManager:
    def __init__(self):
        self.base_directory = "collections_raw_data"
        self.json_directory = os.path.join(self.base_directory, "json_files")
        self.csv_directory = os.path.join(self.base_directory, "csv_files")

        # create directories for raw collections data if doesnt exist
        if not os.path.exists(self.base_directory):
            os.mkdir(self.base_directory)

        if not os.path.exists(self.json_directory):
            os.mkdir(self.json_directory)

        if not os.path.exists(self.csv_directory):
            os.mkdir(self.csv_directory)

    # writes data in json format in a new file everytime executed for version controlling
    def json_writer(self, filename, data):
        timestamp = self.get_timestamp()

        file_path = os.path.join(
            self.json_directory, f"{filename}_{timestamp}.json")
        with open(file_path, "a") as json_file:
            json.dump(data, json_file, indent=4)

    def json_reader(self, filename=None):
        if filename is None:
            filename = self.get_most_recent_file(self.json_directory, ".json")
        else:
            filename += ".json"

        file_path = os.path.join(self.json_directory, f"{filename}")
        with open(file_path, "r") as json_file:
            return json.dumps(json.load(json_file), indent=4)

    # writes data in csv format in a new file everytime executed for version controlling
    def csv_writer(self, filename, data):
        timestamp = self.get_timestamp()

        file_path = os.path.join(
            self.csv_directory, f"{filename}_{timestamp}.csv")

        header = data['collections'][0].keys()

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file, fieldnames=header, quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writeheader()
            for row in data['collections']:
                writer.writerow(row)

    def csv_reader(self, filename=None):
        if filename is None:
            filename = self.get_most_recent_file(self.csv_directory, ".csv")
        else:
            filename += ".csv"

        file_path = os.path.join(self.csv_directory, f"{filename}")
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = [row for row in reader]
            return json.dumps(rows, indent=4)

    # gets current time. for file version controlling
    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    # gets recent file if no file name provided
    def get_most_recent_file(self, directory, extension):
        files = [f for f in os.listdir(directory) if f.endswith(extension)]

        if not files:
            return None

        files.sort(reverse=True)
        return files[0]
