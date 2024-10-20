
"""Library to Tackle the most frequently CSV conversions"""

import csv
import json
import tempfile
import logging
import time
from zipfile import ZipFile
from dataclasses import dataclass

logger = logging.getLogger('simple_example')
logger.setLevel(logging.INFO)


@dataclass
class CSVHandler:
    """
    Module to handle the most frequent csv file manipulations:
        file_path: the path where the original file is located
        csv_encoding: the encoding of the original csv file
        csv_delimiter: the delimiter of the original csv file
    """
    file_path: str
    csv_encoding: str
    csv_delimiter: str

    def change_csv_delimiters(self, output_file, new_delimiter):
        """
        reads a CSV file and writes its content to a new CSV with the wanted delimiter
            :param output_file: full path where the updated file should be saved
            :param new_delimiter: delimiter with which the updated file should be saved
        """
        with open(self.file_path, 'r', encoding=self.csv_encoding) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=self.csv_delimiter)
            with open(output_file, 'w', newline='', encoding="utf8") as output_csv_file:
                writer = csv.DictWriter(output_csv_file, reader.fieldnames, delimiter=new_delimiter)
                writer.writeheader()
                writer.writerows(reader)
        logging.info(f"Converting {self.file_path} to {output_file} complete")

    def csv_to_pretty_json(self, json_file_path):
        """
        converts a CSV file to pretty json
            :param json_file_path: file path where the json file should be saved
        """
        with open(self.file_path, 'r', encoding=self.csv_encoding) as csv_file:
            csv_reader = csv.DictReader(csv_file,  delimiter=self.csv_delimiter)
            data = [row for row in csv_reader]

        with open(json_file_path, 'w', encoding='UTF-8') as json_file:
            json.dump(data, json_file, indent=4)

    def csv_to_new_line_delimited_json(self, json_file_path):
        """
        converts a CSV file to new json delimited json
            :param json_file_path: file path where the json file should be saved
        """
        with open(self.file_path, 'r', encoding=self.csv_encoding) as csv_file:
            csv_reader = csv.DictReader(csv_file,  delimiter=self.csv_delimiter)
            data = [row for row in csv_reader]

        with open(json_file_path, 'w', encoding='UTF-8') as json_file:
            for record in data:
                if len(record) > 0:
                    json_file.write(json.dumps(record) + '\n')

    def zipped_csv_to_new_line_delimited_json(self, json_local_path):
        """converts zipped csv files to json new line delimited"""
        with ZipFile(self.file_path) as myzip:
            for file in myzip.namelist():
                if file.endswith('.csv'):
                    with myzip.open(file) as f:
                        data = f.read().decode(self.csv_encoding, 'ignore').splitlines()
                        with tempfile.NamedTemporaryFile('w', encoding=self.csv_encoding, delete=True):
                            csv_reader = csv.DictReader(data, delimiter=self.csv_delimiter)
                            print('Constructing a Dictionary started')
                            json_data = [row for row in csv_reader]

                        print('Conversion to new line delimited json started')
                        with open(json_local_path, 'w', encoding='utf-8') as json_file:
                            for record in json_data:
                                if len(record) > 0:
                                    json_file.write(json.dumps(record) + '\n')
                        print(f'Converted file is {json_local_path}')
                else:
                    raise OSError

# Example usage:

data_engineer_jobs = CSVHandler('/Users/angelina.teneva/Documents/DataEngineer.csv', 'UTF-8', ',')
data_engineer_jobs.change_csv_delimiters(
     '/Users/angelina.teneva/Documents/data_engineer_jobs_tabbed.csv',
     '|'
 )

data_engineer_jobs.csv_to_pretty_json(
     '/Users/angelina.teneva/Documents/data_engineer_jobs.json'
 )

data_engineer_jobs.csv_to_new_line_delimited_json(
     '/Users/angelina.teneva/Documents/data_engineer_jobs_new_line_delimited.json'
 )

outbrain = CSVHandler('/Users/angelina.teneva/Downloads/gcp_datasets_Outbrain Kaggle Competition_page_views_sample.csv.zip', 'UTF-8', ',')

start_time = time.time()
outbrain.zipped_csv_to_new_line_delimited_json(
    '/Users/angelina.teneva/Documents/outbrain_comprehension_kaggle.json'
)
end_time = time.time()

print(f'execution time: {end_time-start_time} seconds')

netflix = CSVHandler('/Users/angelina.teneva/Downloads/gcp_datasets_zipped_1000-netflix-shows.zip', 'UTF-8', ',')
netflix.zipped_csv_to_new_line_delimited_json(
     '/Users/angelina.teneva/Documents/netflix_shows.json'
)